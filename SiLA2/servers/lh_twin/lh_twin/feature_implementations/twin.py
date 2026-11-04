"""The Hamilton STAR digital twin behind the LiquidHandlerService SiLA 2 feature.

This module knows nothing about SiLA. It wraps PyLabRobot (PLR) and gives the SiLA feature
implementation (``liquidhandlerservice_impl.py``) a small, synchronous, thread-safe API:
``initialize``, ``pick_up_tips``, ``aspirate``, ``dispense``, ``drop_tips``, ``transfer``,
``deck_layout``, ``well_volumes`` and ``firmware_trace``.

What the twin is made of
------------------------
* **PLR v1 STAR driver** (``pylabrobot.hamilton.star``), the same code that drives a real STAR
  over USB, but built on ``STARSimulationDriver``. Instead of writing to a USB link, that driver
  assembles the real firmware command strings (``C0TP...``, ``C0AS...``) and answers the read
  commands (``C0RY``, ``P1RD``...) from PLR's resource model, starting from a recorded real STAR
  configuration (8 x 1000 uL channels, 96-head, iSWAP, autoload).
* **PLR resource model**: the deck, carriers, a tip rack and four plates, with volume and tip
  tracking switched on, so every aspirate/dispense moves liquid between wells and tips.
* **Firmware trace**: every command string the driver "sends" and the simulator's answer, captured
  in memory (see ``_install_firmware_trace``).

Threading model
---------------
PLR is ``async``; the sila2 server calls feature methods from a thread pool. The twin owns ONE
asyncio event loop running forever in a daemon thread, and every PLR coroutine is handed to it
with ``asyncio.run_coroutine_threadsafe(coro, loop).result()``. A ``threading.Lock`` makes sure
only one liquid-handling operation runs at a time (a real STAR also does one thing at a time).

Deck (resource names are part of the PLAN.md contract)
------------------------------------------------------
* ``tip_car`` (Hamilton tip carrier L5, track 1), site 0: ``tips`` (96 x 300 uL filter tips)
* ``plate_car`` (Hamilton plate carrier L5 AC, track 7), sites 0-3:
  ``compounds`` 200 uL/well, ``nadph`` 200 uL/well, ``reaction`` 300 uL/well, ``quench`` 150 uL/well.
  All four are Corning 96 deep-well plates (``cor_96_wellplate_2mL_Vb``, ~2.4 mL/well), because the
  reaction wells reach 400 uL during the workflow (more than a 360 uL standard plate holds).
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from pylabrobot.hamilton.star import STAR, STARDevice, STARSimulationDriver
from pylabrobot.hamilton.star.device import RECORDING_STAR
from pylabrobot.resources import (
  Plate,
  TipRack,
  cor_96_wellplate_2mL_Vb,
  hamilton_96_tiprack_300uL_filter,
  hamilton_plate_carrier_L5_ac,
  hamilton_tip_carrier_L5,
  set_tip_tracking,
  set_volume_tracking,
)
from pylabrobot.resources.errors import ResourceNotFoundError
from pylabrobot.resources.hamilton import STARDeck

# ---------------------------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------------------------

NUM_CHANNELS = 8  # the twin pipettes whole plate columns with 8 channels
NUM_COLUMNS = 12
ROWS = "ABCDEFGH"

PLR_COMMIT_FALLBACK = "7779f506d12755f5f274b4c5cab4d095f4fccb62"

# The simulator can wait out the time the drives would take for each move ("motion time").
# 1.0 = real STAR speed, 0.1 = ten times faster, 0 = no waiting at all. A little motion time
# makes the twin feel like an instrument (and lets SiLA clients see each Transfer step arrive);
# the default keeps a full Transfer well under a second.
MOTION_TIME_SCALE = float(os.environ.get("LH_TWIN_MOTION_SCALE", "0.1"))


@dataclass(frozen=True)
class PlateSpec:
  """One plate of the POC deck: where it sits and what each well starts with."""

  site: int  # plate carrier site; PLR numbers sites from the front (0) to the back (4)
  name: str
  fill_ul: float
  contents: str


TIP_CARRIER_NAME, TIP_CARRIER_TRACK = "tip_car", 1
TIP_RACK_NAME = "tips"
PLATE_CARRIER_NAME, PLATE_CARRIER_TRACK = "plate_car", 7
PLATES: Tuple[PlateSpec, ...] = (
  PlateSpec(0, "compounds", 200.0, "test compounds"),
  PlateSpec(1, "nadph", 200.0, "NADPH cofactor"),
  PlateSpec(2, "reaction", 300.0, "microsomes in buffer (conceptually on the heater-shaker)"),
  PlateSpec(3, "quench", 150.0, "cold acetonitrile"),
)
PLATE_MODEL = "cor_96_wellplate_2mL_Vb"
TIP_RACK_MODEL = "hamilton_96_tiprack_300uL_filter"


def plr_commit() -> str:
  """The PyLabRobot commit actually installed (read from pip's ``direct_url.json``)."""
  try:
    from importlib.metadata import distribution  # noqa: PLC0415

    info = json.loads(distribution("pylabrobot").read_text("direct_url.json") or "{}")
    return info.get("vcs_info", {}).get("commit_id", PLR_COMMIT_FALLBACK)
  except Exception:  # noqa: BLE001 - metadata is a nicety, never a reason to fail
    return PLR_COMMIT_FALLBACK


# ---------------------------------------------------------------------------------------------
# Errors (SiLA-free; the feature implementation maps them to defined execution errors)
# ---------------------------------------------------------------------------------------------


class TwinNotInitializedError(RuntimeError):
  """An operation was requested before ``initialize``."""


class TwinError(RuntimeError):
  """The twin refused or failed an operation; the message says why."""


StatusCallback = Callable[[str], None]
StepCallback = Callable[[int, int, str], None]  # (step number, total steps, description)


# ---------------------------------------------------------------------------------------------
# The twin
# ---------------------------------------------------------------------------------------------


class STARTwin:
  """A simulated Hamilton STAR with the POC deck, driven synchronously from any thread."""

  def __init__(self, on_status: Optional[StatusCallback] = None) -> None:
    self._on_status = on_status or (lambda status: None)

    # One asyncio loop for all PLR coroutines, alive for the whole server lifetime.
    self._loop = asyncio.new_event_loop()
    self._loop_thread = threading.Thread(target=self._loop.run_forever, name="plr-asyncio", daemon=True)
    self._loop_thread.start()

    self._op_lock = threading.Lock()  # one liquid-handling operation at a time
    self._trace_lock = threading.Lock()  # the trace is appended on the loop thread, read elsewhere
    self._trace: List[Dict[str, Any]] = []
    self._current_operation = "none"

    self.star: Optional[STARDevice] = None
    self.setup_summary = ""
    self._used_tip_columns: set[int] = set()  # columns of `tips` already picked up once
    self._mounted_tip_rack = TIP_RACK_NAME  # where the mounted tips came from (rack, column)
    self._mounted_tip_column: Optional[int] = None

  # -- plumbing ---------------------------------------------------------------------------------

  def _run(self, coro: Any, timeout: float = 120.0) -> Any:
    """Run a PLR coroutine on the twin's event loop and wait for its result (blocking)."""
    return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)

  def _operation(self, name: str, func: Callable[[], Any]) -> Any:
    """Run one twin operation under the lock and keep the ``Status`` text up to date.

    Status is "busy: <operation>" while it runs, "idle" afterwards, or "error: <message>" if it
    failed (until the next operation starts).
    """
    with self._op_lock:
      self._current_operation = name
      self._on_status(f"busy: {name}")
      try:
        result = func()
      except Exception as error:
        self._on_status(f"error: {error}")
        raise
      finally:
        self._current_operation = "none"
      self._on_status("idle")
      return result

  def _require_initialized(self) -> STARDevice:
    if self.star is None:
      raise TwinNotInitializedError("Call Initialize before liquid handling.")
    return self.star

  # -- firmware trace ---------------------------------------------------------------------------

  def _install_firmware_trace(self, driver: STARSimulationDriver) -> None:
    """Capture every firmware exchange without modifying PyLabRobot.

    ``STARSimulationDriver._send`` assembles each firmware command string exactly as the real
    driver would put it on the USB link, asks the simulated modules for an answer, and then calls
    ``self._log_exchange(written, read)`` - the same place a real transport logs its writes and
    reads. We shadow that one method *on this driver instance* with a wrapper that records the
    exchange and then calls the original, so PLR's own logging is unchanged.

    ``read`` is None for commands that only move (the simulator has nothing to answer), and a
    text like ``"simulation: {'ry': [...]} from model ..."`` for read commands.
    """
    original = driver._log_exchange  # bound method of this instance

    def recording_log_exchange(written: str, read: Optional[str]) -> None:
      with self._trace_lock:
        self._trace.append(
          {
            "index": len(self._trace),
            "time": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "command": written,
            "reply": read,
            "operation": self._current_operation,
          }
        )
      original(written, read)

    driver._log_exchange = recording_log_exchange  # type: ignore[method-assign]

  def firmware_trace(self, since_index: int = 0) -> List[Dict[str, Any]]:
    """Trace entries with ``index >= since_index`` (empty before Initialize)."""
    with self._trace_lock:
      return [dict(entry) for entry in self._trace[max(since_index, 0) :]]

  # -- building the deck ------------------------------------------------------------------------

  @staticmethod
  def _build_star() -> Tuple[STARDevice, STARSimulationDriver]:
    """Create the simulated STAR and load the POC deck (no firmware traffic yet)."""
    # Volume tracking: every well and tip keeps a volume; aspirate/dispense move liquid.
    # Tip tracking: every tip spot knows whether it still holds a tip.
    set_volume_tracking(True)
    set_tip_tracking(True)

    deck = STARDeck(name="STAR_deck")
    driver = STARSimulationDriver(
      deck=deck,
      declared_configuration_json=RECORDING_STAR,  # a recorded, real STAR configuration
      simulate_motion_time=MOTION_TIME_SCALE > 0,
      motion_time_scale=MOTION_TIME_SCALE if MOTION_TIME_SCALE > 0 else 1.0,
    )
    star = STAR(deck=deck, driver=driver)

    tip_carrier = hamilton_tip_carrier_L5(TIP_CARRIER_NAME)
    tip_carrier[0] = hamilton_96_tiprack_300uL_filter(TIP_RACK_NAME)
    plate_carrier = hamilton_plate_carrier_L5_ac(PLATE_CARRIER_NAME)
    for spec in PLATES:
      plate = cor_96_wellplate_2mL_Vb(spec.name)
      plate_carrier[spec.site] = plate
      for well in plate.children:
        well.tracker.set_volume(spec.fill_ul)

    # A STAR deck has 54 tracks (22.5 mm each); carriers are placed by track number.
    deck.assign_child_resource(tip_carrier, track=TIP_CARRIER_TRACK)
    deck.assign_child_resource(plate_carrier, track=PLATE_CARRIER_TRACK)
    return star, driver

  # -- public operations ------------------------------------------------------------------------

  def initialize(self) -> str:
    """(Re)build the twin and run PLR's STAR setup (firmware discovery + initialisation).

    Calling it again starts over with a fresh deck: full plates, a full tip rack. The firmware
    trace keeps growing (indices stay unique), so a re-initialisation shows up in it.
    """

    def run() -> str:
      if self.star is not None:
        old, self.star = self.star, None
        try:
          self._run(old.stop())
        except Exception:  # noqa: BLE001 - the old twin is being thrown away anyway
          pass

      async def build_and_setup() -> STARDevice:
        star, driver = self._build_star()
        self._install_firmware_trace(driver)
        await star.setup()
        return star

      trace_start = len(self._trace)
      try:
        star = self._run(build_and_setup())
      except Exception as error:
        raise TwinError(f"STAR setup failed: {type(error).__name__}: {error}") from error
      self.star = star
      self._used_tip_columns.clear()
      self._mounted_tip_column = None
      self.setup_summary = star.driver.format_setup_summary()

      plates = ", ".join(f"{p.name} ({p.fill_ul:g} uL/well)" for p in PLATES)
      return (
        f"STAR twin initialised: {len(self._trace) - trace_start} firmware commands exchanged with the "
        f"simulator. Deck: {TIP_RACK_NAME} (96 x 300 uL filter tips) on {TIP_CARRIER_NAME} track "
        f"{TIP_CARRIER_TRACK}; {plates} on {PLATE_CARRIER_NAME} track {PLATE_CARRIER_TRACK}.\n"
        f"{self.setup_summary}"
      )

    return self._operation("Initialize", run)

  def pick_up_tips(self, rack_name: str, column: int) -> str:
    return self._operation(f"PickUpTips {rack_name} column {column}", lambda: self._pick_up(rack_name, column))

  def aspirate(self, plate_name: str, column: int, volume_ul: float) -> str:
    return self._operation(
      f"Aspirate {volume_ul:g} uL from {plate_name} column {column}",
      lambda: self._aspirate(plate_name, column, volume_ul),
    )

  def dispense(self, plate_name: str, column: int, volume_ul: float) -> str:
    return self._operation(
      f"Dispense {volume_ul:g} uL into {plate_name} column {column}",
      lambda: self._dispense(plate_name, column, volume_ul),
    )

  def drop_tips(self) -> str:
    return self._operation("DropTips", self._drop)

  def transfer(
    self,
    source: str,
    source_column: int,
    target: str,
    target_column: int,
    volume_ul: float,
    on_step: Optional[StepCallback] = None,
  ) -> str:
    """Fresh tips -> aspirate -> dispense -> drop tips, reporting each step via ``on_step``.

    The tips come from the next column of ``tips`` that has never been used. If a step fails
    after the tips were picked up, the twin puts them back so it stays usable.
    """
    on_step = on_step or (lambda n, total, text: None)
    label = f"Transfer {volume_ul:g} uL {source} col {source_column} -> {target} col {target_column}"

    def run() -> str:
      self._require_initialized()
      # Validate everything up front, so a bad request does not leave tips on the channels.
      self._get_plate(source)
      self._get_plate(target)
      self._check_column(source_column)
      self._check_column(target_column)
      self._check_volume(volume_ul)
      tip_column = self._next_unused_tip_column()

      steps = [
        (f"pick up tips: {TIP_RACK_NAME} column {tip_column}", lambda: self._pick_up(TIP_RACK_NAME, tip_column)),
        (
          f"aspirate {volume_ul:g} uL x8 from {source} column {source_column}",
          lambda: self._aspirate(source, source_column, volume_ul),
        ),
        (
          f"dispense {volume_ul:g} uL x8 into {target} column {target_column}",
          lambda: self._dispense(target, target_column, volume_ul),
        ),
        ("drop tips: back to their rack spots", self._drop),
      ]
      done: List[str] = []
      try:
        for number, (text, action) in enumerate(steps, start=1):
          on_step(number, len(steps), text)
          action()
          done.append(text)
      except Exception:
        self._try_put_tips_back()
        raise
      return f"{label}: done ({'; '.join(done)})."

    return self._operation(label, run)

  def well_volumes(self, plate_name: str) -> Dict[str, float]:
    """``{"A1": 150.0, "A2": ...}`` from the volume tracker, row by row."""
    with self._op_lock:  # read a consistent state, not one in the middle of an aspirate
      self._require_initialized()
      plate = self._get_plate(plate_name)
      return {
        f"{row}{col}": round(plate.get_well(f"{row}{col}").tracker.get_used_volume(), 3)
        for row in ROWS[: plate.num_items_y]
        for col in range(1, plate.num_items_x + 1)
      }

  def deck_layout(self) -> Dict[str, Any]:
    """The deck as a JSON-ready tree, plus a short summary of the POC resources."""
    with self._op_lock:
      star = self._require_initialized()
      deck = star.deck
      return {
        "deck": deck.name,
        "deck_type": type(deck).__name__,
        "num_tracks": deck.num_tracks,
        "poc_layout": {
          TIP_CARRIER_NAME: {"track": TIP_CARRIER_TRACK, "sites": {"0": TIP_RACK_NAME}},
          PLATE_CARRIER_NAME: {
            "track": PLATE_CARRIER_TRACK,
            "sites": {str(p.site): p.name for p in PLATES},
          },
          "plates": {
            p.name: {"model": PLATE_MODEL, "initial_ul_per_well": p.fill_ul, "contents": p.contents} for p in PLATES
          },
          "tip_columns_used": sorted(self._used_tip_columns),
        },
        "tree": _resource_node(deck),
      }

  def shutdown(self) -> None:
    """Put the simulated STAR down and stop the event loop (called when the server stops)."""
    if self.star is not None:
      try:
        self._run(self.star.stop(), timeout=10)
      except Exception:  # noqa: BLE001
        pass
      self.star = None
    self._loop.call_soon_threadsafe(self._loop.stop)

  # -- the four primitive steps (called with the lock held) -------------------------------------

  def _pick_up(self, rack_name: str, column: int) -> str:
    star = self._require_initialized()
    rack = self._get_tip_rack(rack_name)
    self._check_column(column)
    if self._mounted_tips():
      raise TwinError("tips are already mounted; drop them before picking up new ones")
    spots = rack[f"A{column}:H{column}"]
    missing = [spot.get_identifier() for spot in spots if not spot.has_tip()]
    if missing:
      raise TwinError(f"no tips in {rack_name} at {', '.join(missing)} (out of tips in column {column})")
    self._call_plr(star.pipettes.pick_up_tips(spots))
    if rack_name == TIP_RACK_NAME:
      self._used_tip_columns.add(column)
    self._mounted_tip_column = column
    self._mounted_tip_rack = rack_name
    return f"Picked up 8 tips from {rack_name} column {column}."

  def _aspirate(self, plate_name: str, column: int, volume_ul: float) -> str:
    star = self._require_initialized()
    plate = self._get_plate(plate_name)
    self._check_column(column)
    self._check_volume(volume_ul)
    tips = self._require_tips("aspirate")
    wells = plate[f"A{column}:H{column}"]
    # PLR's simulator would happily draw air from an empty well (it only logs a warning), so the
    # twin checks the tracked volume first and refuses, as a liquid-level check would.
    short = [w.get_identifier() for w in wells if w.tracker.get_used_volume() + 1e-9 < volume_ul]
    if short:
      have = min(w.tracker.get_used_volume() for w in wells)
      raise TwinError(
        f"too little liquid: {volume_ul:g} uL requested from {plate_name} column {column}, "
        f"but {', '.join(short)} hold only {have:g} uL"
      )
    room = min(tip.maximal_volume - tip.tracker.get_used_volume() for tip in tips)
    if volume_ul > room:
      raise TwinError(f"tip overflow: {volume_ul:g} uL requested but the tips only have room for {room:g} uL")
    self._call_plr(star.pipettes.aspirate(wells, volumes=[volume_ul] * NUM_CHANNELS))
    return f"Aspirated {volume_ul:g} uL with 8 channels from {plate_name} column {column}."

  def _dispense(self, plate_name: str, column: int, volume_ul: float) -> str:
    star = self._require_initialized()
    plate = self._get_plate(plate_name)
    self._check_column(column)
    self._check_volume(volume_ul)
    tips = self._require_tips("dispense")
    in_tip = min(tip.tracker.get_used_volume() for tip in tips)
    if in_tip + 1e-9 < volume_ul:
      raise TwinError(f"too little liquid in the tips: {volume_ul:g} uL requested, tips hold {in_tip:g} uL")
    wells = plate[f"A{column}:H{column}"]
    full = [w.get_identifier() for w in wells if w.tracker.get_free_volume() + 1e-9 < volume_ul]
    if full:
      raise TwinError(f"well overflow: {', '.join(full)} of {plate_name} cannot take {volume_ul:g} uL more")
    self._call_plr(star.pipettes.dispense(wells, volumes=[volume_ul] * NUM_CHANNELS))
    return f"Dispensed {volume_ul:g} uL with 8 channels into {plate_name} column {column}."

  def _drop(self) -> str:
    star = self._require_initialized()
    self._require_tips("drop")
    column, rack_name = self._mounted_tip_column, self._mounted_tip_rack
    if column is None:
      raise TwinError("tips are mounted but the twin does not know where they came from")
    rack = self._get_tip_rack(rack_name)
    self._call_plr(star.pipettes.drop_tips(rack[f"A{column}:H{column}"]))
    self._mounted_tip_column = None
    return f"Returned 8 tips to {rack_name} column {column}."

  # -- helpers ----------------------------------------------------------------------------------

  def _call_plr(self, coro: Any) -> Any:
    """Run a PLR pipetting coroutine; turn whatever PLR raises into a ``TwinError``."""
    try:
      return self._run(coro)
    except TwinError:
      raise
    except Exception as error:  # e.g. HasTipError, NoTipError, TooLittleLiquidError, ValueError
      raise TwinError(f"PyLabRobot refused: {type(error).__name__}: {error}") from error

  def _mounted_tips(self) -> list:
    star = self._require_initialized()
    tips = [star.pipettes.get_mounted_tip(ch) for ch in range(NUM_CHANNELS)]
    return [t for t in tips if t is not None]

  def _require_tips(self, action: str) -> list:
    tips = self._mounted_tips()
    if len(tips) < NUM_CHANNELS:
      raise TwinError(f"cannot {action}: no tips mounted on the channels (pick up tips first)")
    return tips

  def _try_put_tips_back(self) -> None:
    """Best-effort cleanup after a failed Transfer step."""
    try:
      if self._mounted_tips() and self._mounted_tip_column is not None:
        self._drop()
    except Exception:  # noqa: BLE001 - the original error is the one to report
      pass

  def _next_unused_tip_column(self) -> int:
    for column in range(1, NUM_COLUMNS + 1):
      if column not in self._used_tip_columns:
        return column
    raise TwinError(f"out of tips: all {NUM_COLUMNS} columns of '{TIP_RACK_NAME}' have been used")

  def _get_resource(self, name: str) -> Any:
    star = self._require_initialized()
    try:
      return star.deck.get_resource(name)
    except ResourceNotFoundError:
      known = ", ".join([TIP_RACK_NAME] + [p.name for p in PLATES])
      raise TwinError(f"unknown resource '{name}' (deck has: {known})") from None

  def _get_plate(self, name: str) -> Plate:
    resource = self._get_resource(name)
    if not isinstance(resource, Plate):
      raise TwinError(f"'{name}' is a {type(resource).__name__}, not a plate")
    return resource

  def _get_tip_rack(self, name: str) -> TipRack:
    resource = self._get_resource(name)
    if not isinstance(resource, TipRack):
      raise TwinError(f"'{name}' is a {type(resource).__name__}, not a tip rack")
    return resource

  @staticmethod
  def _check_column(column: int) -> None:
    if not 1 <= column <= NUM_COLUMNS:
      raise TwinError(f"column must be 1-{NUM_COLUMNS}, got {column}")

  @staticmethod
  def _check_volume(volume_ul: float) -> None:
    if not volume_ul > 0:
      raise TwinError(f"volume must be > 0 uL, got {volume_ul:g}")


def _resource_node(resource: Any, depth: int = 0) -> Dict[str, Any]:
  """Describe one PLR resource and (down to plates and tip racks) its children.

  PLR models the deck as a tree: deck -> carrier -> site (holder) -> plate/tip rack -> wells/tip
  spots. Wells and tip spots are summarised, not listed (96 entries each would drown the rest).
  ``location`` is relative to the parent, ``absolute_location`` is in deck coordinates (mm).
  """

  def xyz(c: Any) -> Optional[Dict[str, float]]:
    return None if c is None else {"x": round(c.x, 2), "y": round(c.y, 2), "z": round(c.z, 2)}

  node: Dict[str, Any] = {
    "name": resource.name,
    "type": type(resource).__name__,
    "category": resource.category,
    "model": resource.model,
    "location": xyz(resource.location),
    "absolute_location": xyz(resource.get_absolute_location()) if resource.parent is not None else None,
    "size": {
      "x": round(resource.get_absolute_size_x(), 2),
      "y": round(resource.get_absolute_size_y(), 2),
      "z": round(resource.get_absolute_size_z(), 2),
    },
  }
  if isinstance(resource, Plate):
    node["wells"] = len(resource.children)
    node["well_max_volume_ul"] = round(resource.get_well("A1").max_volume, 1)
    return node
  if isinstance(resource, TipRack):
    node["tip_spots"] = len(resource.children)
    node["tips_present"] = sum(1 for spot in resource.children if spot.has_tip())
    return node
  if depth < 4:
    node["children"] = [_resource_node(child, depth + 1) for child in resource.children]
  return node


__all__ = ["STARTwin", "TwinError", "TwinNotInitializedError", "plr_commit", "MOTION_TIME_SCALE", "PLATES"]
