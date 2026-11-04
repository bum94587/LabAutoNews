"""
First-order thermal model of a heater-shaker block (pure Python, no SiLA here).

The block temperature T follows Newton-style first-order dynamics towards the setpoint:

    dT/dt = (T_target - T) / tau

with tau = 30 s of *simulated* time. The twin runs on accelerated time (factor 10), so one
real second is ten simulated seconds and a 22 -> 37 C ramp takes about 10 real seconds.

Instead of integrating step by step (which would make the result depend on how often someone
asks), the model uses the exact solution of the ODE over each elapsed interval:

    T(t + dt) = T_target + (T(t) - T_target) * exp(-dt / tau)

so reading the temperature at any moment, from any thread, gives the same physics.

The class is thread-safe: the SiLA server reads it from a background "tick" thread, from the
SetTemperature command thread and from property requests at the same time.
"""

from __future__ import annotations

import math
import threading
import time
from typing import Callable, Optional

#: Contract values from PLAN.md
TAU_SIM_S: float = 30.0  # time constant, simulated seconds
TIME_ACCELERATION: float = 10.0  # simulated seconds per real second
START_TEMPERATURE_C: float = 22.0  # block starts at room temperature
REACHED_TOLERANCE_C: float = 0.5  # "reached" when |T - target| <= this


class ThermalModel:
    """
    Thread-safe first-order thermal model running on accelerated time.

    Parameters
    ----------
    tau_s
        Time constant in simulated seconds.
    acceleration
        Simulated seconds per real second.
    start_c
        Initial block temperature (also the initial setpoint, i.e. "heater idle").
    tolerance_c
        Band around the setpoint that counts as "reached".
    clock
        Monotonic clock in real seconds (injectable for testing).
    """

    def __init__(
        self,
        tau_s: float = TAU_SIM_S,
        acceleration: float = TIME_ACCELERATION,
        start_c: float = START_TEMPERATURE_C,
        tolerance_c: float = REACHED_TOLERANCE_C,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.tau_s = tau_s
        self.acceleration = acceleration
        self.tolerance_c = tolerance_c
        self._clock = clock
        self._lock = threading.Lock()
        self._temperature = start_c
        self._target = start_c
        self._last_update = clock()
        # Incremented on every new setpoint, so a waiting command can tell if it was superseded.
        self._generation = 0

    # --- internal ---------------------------------------------------------------------------

    def _advance_locked(self) -> None:
        """Advance the model to 'now' using the exact exponential solution. Caller holds the lock."""
        now = self._clock()
        dt_sim = (now - self._last_update) * self.acceleration
        self._last_update = now
        if dt_sim > 0:
            self._temperature = self._target + (self._temperature - self._target) * math.exp(-dt_sim / self.tau_s)

    # --- public API -------------------------------------------------------------------------

    def set_target(self, target_c: float) -> int:
        """
        Change the setpoint. Returns the new setpoint generation number.

        The temperature reached so far is preserved: the model is advanced to "now" under the
        old setpoint before switching to the new one.
        """
        with self._lock:
            self._advance_locked()
            self._target = float(target_c)
            self._generation += 1
            return self._generation

    @property
    def generation(self) -> int:
        """Setpoint generation (changes whenever set_target is called)."""
        with self._lock:
            return self._generation

    @property
    def target(self) -> float:
        """Current setpoint in C."""
        with self._lock:
            return self._target

    @property
    def temperature(self) -> float:
        """Current block temperature in C (advances the model to 'now' first)."""
        with self._lock:
            self._advance_locked()
            return self._temperature

    def snapshot(self) -> tuple[float, float, int]:
        """Consistent (temperature, target, generation) triple, read under one lock."""
        with self._lock:
            self._advance_locked()
            return self._temperature, self._target, self._generation

    def is_reached(self, temperature: Optional[float] = None, target: Optional[float] = None) -> bool:
        """True when the block is within the tolerance band of the setpoint."""
        if temperature is None or target is None:
            temperature, target, _ = self.snapshot()
        return abs(temperature - target) <= self.tolerance_c

    def real_seconds_to_reach(self, temperature: float, target: float) -> float:
        """
        Predicted real time until |T - target| <= tolerance, from the analytic solution:
        |T - target| * exp(-t/tau) = tolerance  ->  t = tau * ln(|T - target| / tolerance).
        """
        gap = abs(temperature - target)
        if gap <= self.tolerance_c:
            return 0.0
        return self.tau_s * math.log(gap / self.tolerance_c) / self.acceleration
