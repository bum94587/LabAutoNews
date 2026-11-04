"""
SiLA 2 implementation of the ``HeaterShakerService`` feature for the heater-shaker digital twin.

The feature definition (FDL, ``features/HeaterShakerService-v1_0.sila.xml``) is the contract;
``sila2-codegen`` turned it into the abstract base class ``HeaterShakerServiceBase`` and this
file fills in the behaviour. SiLA concepts used here:

* **Observable command** (``SetTemperature``): a long-running command. The client gets a
  Command Execution UUID straight away, then can (a) subscribe to *execution info* (status,
  progress, estimated remaining time), (b) subscribe to *intermediate responses* (here: the
  current temperature while ramping) and (c) fetch the final *response* once it has finished
  (here: ``ReachedTemperature``). The sila2 library runs our method in a worker thread and
  passes an ``instance`` object we use to publish (a) and (b).
* **Unobservable commands** (``StartShaking``, ``StopShaking``): plain request/response calls.
* **Observable property** (``CurrentTemperature``): clients *subscribe* and receive a new value
  every time the server publishes one with the generated ``update_CurrentTemperature(...)``.
* **Unobservable property** (``ShakingSpeed``): read on request via ``get_ShakingSpeed``.
* **Defined execution errors** (``TemperatureOutOfRange``, ``SpeedOutOfRange``): errors named
  in the FDL, so clients can handle them specifically. We raise the generated classes; any
  other exception reaches the client as an *undefined* execution error.

The physics lives in :mod:`.thermal`; the model evolves continuously, and a background tick
(registered with ``run_periodically``) publishes the observable property and logs state changes.
"""

from __future__ import annotations

import logging
import threading
from datetime import timedelta
from typing import TYPE_CHECKING

from sila2.framework import UndefinedExecutionError
from sila2.server import MetadataDict, ObservableCommandInstanceWithIntermediateResponses

from ..generated.heatershakerservice import (
    HeaterShakerServiceBase,
    SetTemperature_IntermediateResponses,
    SetTemperature_Responses,
    SpeedOutOfRange,
    StartShaking_Responses,
    StopShaking_Responses,
    TemperatureOutOfRange,
)
from .thermal import ThermalModel

if TYPE_CHECKING:
    from ..server import Server

#: Allowed ranges (must match the error descriptions in the FDL)
MIN_TEMPERATURE_C, MAX_TEMPERATURE_C = 4.0, 70.0
MIN_SPEED_RPM, MAX_SPEED_RPM = 200, 3000

#: Real seconds between model ticks / intermediate responses
TICK_S: float = 0.25

#: Observable-property values are rounded to this many decimals; a new value is only
#: published when the rounded value changes (so a stable block does not flood subscribers).
PUBLISH_DECIMALS: int = 2

# State-change log for the run results. The server's default log level is WARNING, so give this
# logger its own INFO level; records still go to the root handler that __main__ configures.
logger = logging.getLogger("hhs_twin.twin")
logger.setLevel(logging.INFO)


class HeaterShakerServiceImpl(HeaterShakerServiceBase):
    """Heater-shaker digital twin: first-order thermal model + a shaker speed setting."""

    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

        # Lifetime of execution (a SiLA concept): how long the server must remember a finished
        # observable command instance so clients can still fetch its result. None = until server
        # shutdown. We use None on purpose: in sila2 0.14 a finite lifetime starts a non-daemon
        # cleanup thread per instance that sleeps until the lifetime expires, which would keep the
        # server process alive that long after shutdown. A POC makes only a few calls, so the
        # memory cost of keeping them is negligible.
        self.SetTemperature_default_lifetime_of_execution = None

        self._model = ThermalModel()
        self._shaker_lock = threading.Lock()
        self._shaking_speed_rpm = 0
        self._stop_event = threading.Event()  # set on server shutdown, ends waiting commands

        # Bookkeeping for the background tick (only touched by the tick thread).
        temperature, target, _ = self._model.snapshot()
        self._last_published = round(temperature, PUBLISH_DECIMALS)
        self._was_reached = self._model.is_reached(temperature, target)

        # Give the observable property an initial value: a new subscriber always receives the
        # most recent value first, then every later update.
        self.update_CurrentTemperature(self._last_published)
        logger.info("Heater-shaker twin ready: T=%.2f C, setpoint %.2f C, shaker stopped", temperature, target)

        # The sila2 base class runs registered functions in a loop on a server worker thread
        # between start() and stop(). This keeps the property live even when no command runs.
        self.run_periodically(self._tick, delay_seconds=TICK_S)

    # --- lifecycle ------------------------------------------------------------------------

    def stop(self) -> None:
        """Called by the SiLA server on shutdown: release any SetTemperature still waiting."""
        self._stop_event.set()
        super().stop()

    # --- background tick ------------------------------------------------------------------

    def _tick(self) -> None:
        """Advance the model, publish the observable property, log reached/left-band events."""
        temperature, target, _ = self._model.snapshot()

        rounded = round(temperature, PUBLISH_DECIMALS)
        if rounded != self._last_published:
            # SiLA observable property: push the new value to every subscribed client.
            self.update_CurrentTemperature(rounded)
            self._last_published = rounded

        reached = self._model.is_reached(temperature, target)
        if reached and not self._was_reached:
            logger.info("Setpoint reached: T=%.2f C (setpoint %.2f C)", temperature, target)
        self._was_reached = reached

    # --- unobservable property --------------------------------------------------------------

    def get_ShakingSpeed(self, *, metadata: MetadataDict) -> int:
        """Unobservable property: current speed in rpm (0 = stopped)."""
        with self._shaker_lock:
            return self._shaking_speed_rpm

    # --- unobservable commands --------------------------------------------------------------

    def StartShaking(self, Speed: int, *, metadata: MetadataDict) -> StartShaking_Responses:
        """Start (or change) orbital shaking. Out-of-range speed -> SpeedOutOfRange (defined error)."""
        if not MIN_SPEED_RPM <= Speed <= MAX_SPEED_RPM:
            logger.warning("StartShaking rejected: %d rpm is outside %d-%d", Speed, MIN_SPEED_RPM, MAX_SPEED_RPM)
            # Defined execution error: the client receives it with its FDL identifier.
            raise SpeedOutOfRange(f"Speed {Speed} rpm is outside {MIN_SPEED_RPM}-{MAX_SPEED_RPM} rpm.")
        with self._shaker_lock:
            previous = self._shaking_speed_rpm
            self._shaking_speed_rpm = Speed
        logger.info("Shaking: %d -> %d rpm", previous, Speed)
        return StartShaking_Responses(Message=f"Shaking at {Speed} rpm (was {previous} rpm)")

    def StopShaking(self, *, metadata: MetadataDict) -> StopShaking_Responses:
        """Stop shaking (idempotent: stopping a stopped shaker is fine)."""
        with self._shaker_lock:
            previous = self._shaking_speed_rpm
            self._shaking_speed_rpm = 0
        logger.info("Shaking stopped (was %d rpm)", previous)
        return StopShaking_Responses(Message=f"Shaking stopped (was {previous} rpm)")

    # --- observable command -----------------------------------------------------------------

    def SetTemperature(
        self,
        TargetTemperature: float,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstanceWithIntermediateResponses[SetTemperature_IntermediateResponses],
    ) -> SetTemperature_Responses:
        """
        Observable command: change the setpoint and wait until the block is within 0.5 C of it.

        While waiting, every TICK_S it sends the current temperature as an *intermediate response*
        and updates the *execution info* (progress 0..1 and estimated remaining time). The return
        value becomes the command's final *response*.
        """
        # Validate before starting. Raising here ends the instance with status `finishedWithError`;
        # the client sees the defined execution error when it asks for the result (get_responses).
        if not MIN_TEMPERATURE_C <= TargetTemperature <= MAX_TEMPERATURE_C:
            logger.warning(
                "SetTemperature rejected: %.2f C is outside %.0f-%.0f C",
                TargetTemperature,
                MIN_TEMPERATURE_C,
                MAX_TEMPERATURE_C,
            )
            raise TemperatureOutOfRange(
                f"Target {TargetTemperature} C is outside {MIN_TEMPERATURE_C:.0f}-{MAX_TEMPERATURE_C:.0f} C."
            )

        # Execution status goes from `waiting` to `running`.
        instance.begin_execution()

        start_temperature = self._model.temperature
        my_generation = self._model.set_target(TargetTemperature)
        start_gap = abs(start_temperature - TargetTemperature)
        logger.info(
            "Setpoint -> %.2f C (T=%.2f C, expect ~%.1f s real)",
            TargetTemperature,
            start_temperature,
            self._model.real_seconds_to_reach(start_temperature, TargetTemperature),
        )

        while True:
            temperature, target, generation = self._model.snapshot()

            # Intermediate response: streamed to clients subscribed to this command instance.
            instance.send_intermediate_response(SetTemperature_IntermediateResponses(CurrentTemperature=temperature))

            # Execution info: progress fraction and the model's own prediction of time left.
            gap = abs(temperature - TargetTemperature)
            instance.progress = 1.0 if start_gap == 0 else min(1.0, max(0.0, 1.0 - gap / start_gap))
            instance.estimated_remaining_time = timedelta(
                seconds=self._model.real_seconds_to_reach(temperature, TargetTemperature)
            )

            if generation != my_generation:
                # Another SetTemperature changed the setpoint; this one can never complete as asked.
                # Not in the FDL, so it is reported as an undefined execution error.
                raise UndefinedExecutionError(
                    f"SetTemperature {TargetTemperature} C superseded by a new setpoint ({target} C)"
                )
            if self._model.is_reached(temperature, TargetTemperature):
                logger.info("SetTemperature %.2f C done: T=%.2f C", TargetTemperature, temperature)
                return SetTemperature_Responses(ReachedTemperature=temperature)
            if self._stop_event.wait(TICK_S):
                raise UndefinedExecutionError("Server shutting down")
