"""SiLA 2 implementation of the LiquidHandlerService feature, backed by the STAR digital twin.

How the pieces fit
------------------
* The **Feature Definition** (``features/LiquidHandlerService-v1_0.sila.xml``) declares the
  commands, properties and errors. ``sila2-codegen`` turned it into ``generated/liquidhandlerservice``:
  a base class with one abstract method per command/property, NamedTuple response types, and the
  defined execution error classes ``NotInitialized`` and ``LiquidHandlingError``.
* This class fills in those methods. Each one is a thin adapter: call the twin
  (``twin.py``, which knows PyLabRobot but not SiLA), wrap the result in the generated response
  type, and translate twin exceptions into SiLA **defined execution errors** - errors a client can
  catch by name because the FDL announces them.
* The sila2 server calls these methods from a thread pool. The twin serialises the actual
  liquid handling, so concurrent client calls simply queue up.

SiLA concepts used here
-----------------------
* Unobservable property ``InstrumentInfo``: a plain getter (``get_InstrumentInfo``).
* Observable property ``Status``: the server keeps a current value and pushes every change to
  subscribed clients; we publish with the generated ``update_Status(...)``.
* Unobservable commands (``Initialize``, ``Aspirate``...): call, block, return a response.
* Observable command ``Transfer``: the client gets a command execution UUID immediately and can
  subscribe to execution info (status/progress) and **intermediate responses** (here: ``Step``
  strings) while it runs, then fetch the final response.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Callable, TypeVar

from sila2.server import MetadataDict, ObservableCommandInstanceWithIntermediateResponses

from ..generated.liquidhandlerservice import (
    Aspirate_Responses,
    Dispense_Responses,
    DropTips_Responses,
    GetDeckLayout_Responses,
    GetFirmwareTrace_Responses,
    GetWellVolumes_Responses,
    Initialize_Responses,
    LiquidHandlerServiceBase,
    LiquidHandlingError,
    NotInitialized,
    PickUpTips_Responses,
    Transfer_IntermediateResponses,
    Transfer_Responses,
)
from .twin import MOTION_TIME_SCALE, PLATES, STARTwin, TwinError, TwinNotInitializedError, plr_commit

if TYPE_CHECKING:
    from ..server import Server

T = TypeVar("T")


def _call_twin(func: Callable[[], T]) -> T:
    """Run a twin call and map its exceptions to the feature's defined execution errors.

    Anything else that escapes (a bug) is turned into an *undefined* execution error by the sila2
    framework automatically, which is the SiLA way of saying "unexpected server failure".
    """
    try:
        return func()
    except TwinNotInitializedError as error:
        raise NotInitialized(str(error)) from error
    except TwinError as error:
        raise LiquidHandlingError(str(error)) from error


class LiquidHandlerServiceImpl(LiquidHandlerServiceBase):
    """Column-wise 8-channel liquid handling on a simulated Hamilton STAR."""

    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

        # Lifetime of observable command instances (Transfer): None = keep every execution UUID
        # (and its result) until the server stops. A finite timedelta would make the server forget
        # it after that time, but in sila2 0.14 each finite lifetime starts a non-daemon cleanup
        # thread that sleeps until expiry and so blocks process exit; a POC run is short anyway.
        self.Transfer_default_lifetime_of_execution = None

        # The twin calls update_Status whenever its state changes; the sila2 framework forwards
        # each value to every client subscribed to the observable property `Status`.
        # Vocabulary: "not initialized" (until Initialize succeeds), "idle", "busy: <operation>",
        # "error: <message>" (until the next operation starts).
        self.twin = STARTwin(on_status=self.update_Status)
        self.update_Status("not initialized")

    def stop(self) -> None:
        """Called by the sila2 server on shutdown: put the simulated STAR down too."""
        self.twin.shutdown()
        super().stop()

    # -- properties -------------------------------------------------------------------------------

    def get_InstrumentInfo(self, *, metadata: MetadataDict) -> str:
        plates = ", ".join(f"{p.name}={p.fill_ul:g} uL/well" for p in PLATES)
        info = (
            "Model: Hamilton Microlab STAR (digital twin, no hardware). "
            f"Driver: PyLabRobot v1 pylabrobot.hamilton.star.STAR, commit {plr_commit()}. "
            "Simulator: STARSimulationDriver - firmware-level; assembles the real firmware command "
            "strings and answers reads from PLR's resource/volume model, configured from a recorded real "
            "STAR (star_legacy_2021_8ch_head96_autoload1D: 8 x 1000 uL channels, 96-head, iSWAP, autoload). "
            f"Motion time scale: {MOTION_TIME_SCALE:g} (1 = real speed, 0 = instant). "
            "Labware: hamilton_tip_carrier_L5 + hamilton_96_tiprack_300uL_filter; hamilton_plate_carrier_L5_ac + "
            f"4 x cor_96_wellplate_2mL_Vb deep-well plates (deep wells because reaction reaches 400 uL); {plates}."
        )
        if self.twin.setup_summary:
            info += "\n" + self.twin.setup_summary
        return info

    # -- unobservable commands --------------------------------------------------------------------

    def Initialize(self, *, metadata: MetadataDict) -> Initialize_Responses:
        # Initialize declares no defined errors in the FDL, so a failed setup surfaces as an
        # undefined execution error carrying the twin's message.
        try:
            summary = self.twin.initialize()
        except TwinError as error:
            raise RuntimeError(str(error)) from error
        return Initialize_Responses(Summary=summary)

    def GetDeckLayout(self, *, metadata: MetadataDict) -> GetDeckLayout_Responses:
        layout = _call_twin(self.twin.deck_layout)
        return GetDeckLayout_Responses(DeckLayoutJson=json.dumps(layout))

    def PickUpTips(self, TipRack: str, Column: int, *, metadata: MetadataDict) -> PickUpTips_Responses:
        return PickUpTips_Responses(Message=_call_twin(lambda: self.twin.pick_up_tips(TipRack, Column)))

    def Aspirate(self, Plate: str, Column: int, VolumeUl: float, *, metadata: MetadataDict) -> Aspirate_Responses:
        return Aspirate_Responses(Message=_call_twin(lambda: self.twin.aspirate(Plate, Column, VolumeUl)))

    def Dispense(self, Plate: str, Column: int, VolumeUl: float, *, metadata: MetadataDict) -> Dispense_Responses:
        return Dispense_Responses(Message=_call_twin(lambda: self.twin.dispense(Plate, Column, VolumeUl)))

    def DropTips(self, *, metadata: MetadataDict) -> DropTips_Responses:
        return DropTips_Responses(Message=_call_twin(self.twin.drop_tips))

    def GetWellVolumes(self, Plate: str, *, metadata: MetadataDict) -> GetWellVolumes_Responses:
        volumes = _call_twin(lambda: self.twin.well_volumes(Plate))
        return GetWellVolumes_Responses(VolumesJson=json.dumps(volumes))

    def GetFirmwareTrace(self, SinceIndex: int, *, metadata: MetadataDict) -> GetFirmwareTrace_Responses:
        return GetFirmwareTrace_Responses(TraceJson=json.dumps(self.twin.firmware_trace(SinceIndex)))

    # -- observable command -----------------------------------------------------------------------

    def Transfer(
        self,
        SourcePlate: str,
        SourceColumn: int,
        TargetPlate: str,
        TargetColumn: int,
        VolumeUl: float,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstanceWithIntermediateResponses[Transfer_IntermediateResponses],
    ) -> Transfer_Responses:
        # Observable commands start in state "waiting"; tell subscribers we are running now.
        instance.begin_execution()

        def report_step(number: int, total: int, text: str) -> None:
            # Execution info (progress 0..1) and an intermediate response for each sub-step.
            # A client that subscribes late still gets the most recent Step immediately.
            instance.progress = (number - 1) / total
            instance.send_intermediate_response(Transfer_IntermediateResponses(Step=f"{number}/{total} {text}"))

        message = _call_twin(
            lambda: self.twin.transfer(
                SourcePlate, SourceColumn, TargetPlate, TargetColumn, VolumeUl, on_step=report_step
            )
        )
        instance.progress = 1.0
        return Transfer_Responses(Message=message)
