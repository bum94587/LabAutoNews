# Review: SiLA 2 digital-twin POC

Reviewer notes on `PLAN.md`, the FDLs and (phase 2) the builders' code. Priorities:
**blocker** (the demo will fail or hang), **should-fix** (wrong, fragile or misleading),
**nice-to-have** (polish, SiLA good practice, teaching value).

Evidence for the PLR points comes from reading PyLabRobot @ 7779f50 and from a probe script run
in this env (`scratchpad/review/probe.py`): STAR(simulation=True) setup takes ~0.01 s and 148
firmware commands; one 8-channel transfer (pick up, aspirate 50, dispense 50, drop) takes
~0.3 s and 103 firmware commands.

## Phase 1: plan

### Blockers

1. **Reaction plate overflows with the planned labware.** `reaction` starts at 300 uL/well and
   receives 50 (compound) + 50 (NADPH) = 400 uL, but `cor_96_wellplate_360uL_Fb` holds 360 uL.
   PLR refuses the dispense (`ValueError: ... has room for 30.0 uL, not the 50.0 uL`), so step 2/4
   fails. *Fix (LH builder):* put `reaction` on `cor_96_wellplate_2mL_Vb` (verified: works on
   `PLT_CAR_L5AC_A00` in the simulator, 400 uL tracked fine), or start it at 200 uL. Record the
   choice in `InstrumentInfo`/run summary. Volumes are otherwise fine: reaction ends at 150 uL,
   quench wells at 200 uL, 7 tip columns used of 12.

2. **Firmware-trace hook: PLR's event bus does not fire in simulation.** `STARDriver._send`
   (`driver/master.py:590`) emits `firmware.command.*` events, but `STARSimulationDriver._send`
   (`driver/simulator.py` ~line 2066) *replaces* `_send` and never calls `emit_event`. Wrapping
   `send_command` gives module/command/kwargs, not the firmware string. *Fix (LH builder):* wrap
   the instance method `star.driver._log_exchange(written, read)` (verified: it receives every
   assembled command such as `C0RT` and the simulated reply, `read` is `None` for pure moves).
   Alternative: a `logging.Handler` on `pylabrobot.hamilton.star.driver.simulator`, but then the
   logger level must be set to 5 (`LOG_LEVEL_IO`), otherwise nothing arrives (default WARNING).
   Expect ~900 trace entries per demo run; `GetFirmwareTrace(SinceIndex)` should slice, and the
   run summary should report counts rather than dump everything.

3. **Scheduler can deadlock on any failure or ordering mistake.** Per-device FIFO lanes plus
   cross-lane `depends_on` and `start_after_t0_s` will block forever if (a) a step fails and its
   dependants keep waiting, (b) the t0-marking step fails so t0 is never set, or (c) a lane's YAML
   order disagrees with the dependency order (lane A waits on B's step 5, B's lane is stuck on
   step 4 which waits on A's step 6). *Fix (scheduler builder):*
   - At load time add implicit edges lane[i] -> lane[i+1] for each device and run cycle detection
     (Kahn's algorithm); refuse to run a cyclic workflow with a clear message.
   - One `threading.Event` + status per step. A failed step sets its event with status `failed`;
     a step whose dependency failed is marked `skipped` and sets its own event, so everything
     drains. Make every timed step implicitly depend on the step that marks t0.
   - Back-stop: every wait uses a timeout (e.g. 120 s), failing the step instead of hanging.
   - `run_demo.py` exits non-zero if any step is failed/skipped.

4. **`get_responses()` raises if called too early; intermediate responses are best-effort.**
   In sila2 0.14 the server answers `_Result` with `CommandExecutionNotFinished` while the command
   runs (`server/observables/observable_command_manager.py`). A late subscriber to intermediate
   responses only gets the *last* item (`SubscriptionManagerThread.add_subscription` replays one
   item), and a 0.3 s Transfer can finish before the client subscribes. *Fix (scheduler):*
   subscribe immediately after starting, iterate until the stream ends, then
   `while not inst.done: time.sleep(0.05)` (with a timeout) before `inst.get_responses()`; never
   assume all four `Step` items arrive. *Fix (LH):* put the step list in the final `Message` too,
   and optionally a short `time.sleep` per sub-step (<= 0.1 s, see should-fix 6) so streaming is
   visible in the demo.

### Should-fix

1. **Use one persistent asyncio loop thread for PLR, never `asyncio.run` per command.** STAR's
   `_FirmwareLock` holds asyncio primitives bound to the loop that first used them; a second loop
   raises "bound to a different event loop". Create the loop thread in the impl `__init__`/`start()`,
   build the STAR *and* call `setup()` on that loop, and route every PLR call through one helper
   `run(coro, timeout=...)` -> `asyncio.run_coroutine_threadsafe(coro, loop).result(timeout)`. sila2
   calls unobservable commands from up to 100 gRPC worker threads and observable ones from the
   child-task pool, so guard each SiLA command with a `threading.Lock` (hold it around the whole
   operation, including the volume/tip bookkeeping), not only around the coroutine.

2. **Map *all* PLR exceptions to `LiquidHandlingError`.** PLR raises plain `ValueError`
   (overflow), `RuntimeError` (no tip: "channels [...] carry no tip"), `TooLittleLiquidError`, etc.
   Catch `Exception` in the helper and re-raise the generated `LiquidHandlingError(str(e))`;
   otherwise clients see `UndefinedExecutionError`. Also set `Status` to `error: <msg>`.

3. **Transfer must clean up tips on failure.** If dispense fails after pick-up/aspirate, the
   channels still carry tips and every later `PickUpTips`/`Transfer` fails ("tip already
   mounted"). *Fix (LH):* `try: ... except: drop tips (best effort) ; raise LiquidHandlingError`.

4. **One source of truth for tips.** `DropTips` returns tips to their spots, so PLR's tip tracker
   will say the column still "has tips"; the "next unused column" therefore needs a twin-side
   `used_columns` set that both `PickUpTips` and `Transfer` update (or Transfer should drop to
   trash). Out of tips -> `LiquidHandlingError`.

5. **Observable properties need an initial value.** `Status` and `CurrentTemperature` are fed by
   `update_X()`; until the first call a subscriber (and the dynamic client's `.get()`, which
   subscribes and waits for the first item) blocks forever. Call `update_Status("idle (not
   initialized)")` / `update_CurrentTemperature(22.0)` in `__init__`.

6. **Time budget of the timepoints.** With 1 "minute" = 2 s, t = 0, 1, 2, 3 min are 2 s apart and
   each needs StopShaking + Transfer (~0.3 s + gRPC) + StartShaking. Any per-step sleep added for
   visual effect eats into that; keep the added delay per Transfer <= ~0.5 s total, or use 1 min = 4 s.
   The scheduler should record planned vs actual start (lateness) per timed step and print a
   warning when late, rather than silently drifting.

7. **HHS: a superseded `SetTemperature` must not wait forever.** If SetTemperature(37) is still
   running when SetTemperature(22) arrives, the first one never reaches 37 and blocks a child
   thread (and `server.stop()` waits for child tasks with `shutdown(wait=True)`). *Fix:* keep a
   target "generation" counter; a running SetTemperature whose generation is stale returns (or
   raises) immediately. Also have every wait loop check a stop `threading.Event` set in `stop()`.
   Prefer computing T analytically (`T = Tt + (T0 - Tt) * exp(-dt_sim / tau)`) on read, with a
   daemon ticker thread only to push `update_CurrentTemperature` ~5 Hz. Set `instance.progress`
   and `instance.estimated_remaining_time` (closed form: `tau * ln(|T - Tt| / 0.5) / accel`).
   Note: 22 -> 37 C within 0.5 C takes ln(15/0.5) * 3 s = ~10 s real, not "a few seconds".

8. **`Initialize` declares no execution errors.** Any failure (or a defined error raised from it)
   reaches the client as `UndefinedExecutionError`: the dynamic client converts defined errors
   not listed for that command (`client/utils.py`, `rpcerror_to_silaerror`). Make `Initialize`
   idempotent (second call returns the summary) and either accept that, or (lead decision, needs
   FDL + `sila2-codegen update`) add `LiquidHandlingError` to it. Same rule for the builders: only
   raise errors listed on that command (e.g. `GetFirmwareTrace` must not raise `NotInitialized`;
   return `[]`).

9. **Server lifecycle in `run_demo.py` / tests.** The generated `__main__` handles SIGTERM by
   `grpc_server.stop()` then `server.stop()`, which joins the child-task pool and calls
   `impl.stop()`. *Fix:* `proc.terminate(); proc.wait(timeout=10)` then `proc.kill()`; run in
   `try/finally` (also on Ctrl-C). Readiness: TCP accept is not enough on its own; loop
   `SilaClient(host, port, insecure=True)` until it succeeds (PLR import takes seconds), with a
   ~30 s timeout and the server's stderr shown on failure. A startup failure in the generated
   `__main__` logs and *returns 0*, so check readiness, not the exit code. Tests should use free
   ports (`socket.bind(("127.0.0.1", 0))`) so they don't collide with a running demo; give
   `run_demo.py` `--lh-port/--hhs-port`. Implement `impl.stop()` in the LH twin to `await
   star.stop()` and stop/join the loop thread.

10. **Parameter types from YAML.** `Integer` parameters go straight into
    `SiLAFramework_pb2.Integer(value=...)`, so `Column: 1.0` or `Speed: 600.0` raises `TypeError`
    in the client; `Real` accepts ints. Coerce per FDL type in the scheduler (or keep YAML ints).

11. **Fill in `server.py`** name/description/type (currently `"TODO"`); server_type should be
    something like `LiquidHandlerTwin` / `HeaterShakerTwin` (pattern `[A-Z][a-zA-Z0-9]*`).

### Nice-to-have

1. **Units and constraints in the FDL** (post-POC or when the lead next regenerates; Python
   signatures stay `float`/`int`, so `sila2-codegen update` is low-risk): `Column` as Constrained
   Integer `MinimalInclusive 1`/`MaximalInclusive 12`; `VolumeUl` with Unit (Label `uL`, Factor
   1e-9, SIUnit Meter, Exponent 3) and `MinimalExclusive 0`; temperatures with Unit (Label `degC`,
   Factor 1, Offset 273.15, SIUnit Kelvin); `Speed` with Unit (rpm). Constraints make the server
   reject bad input with a `ValidationError` at command initiation, which is the SiLA-idiomatic
   path. If range constraints are added, `TemperatureOutOfRange`/`SpeedOutOfRange` become
   unreachable; keep the errors only if the demo wants to show defined execution errors.
2. **Structured types instead of JSON strings** for `GetWellVolumes` (List of Structure
   `{Well: String, VolumeUl: Real}`) would show SiLA's type system; JSON is fine for a POC but say
   so in the docs.
3. **SiLA core features worth mentioning in the docs:** `SimulationController` (a twin is exactly
   what it is for), `CancelController` (cancel a long SetTemperature), `LockController`.
4. **`Status` vocabulary:** fix the prefixes (`idle`, `busy: <op>`, `error: <msg>`,
   `not initialized`) in the FDL description so clients can parse it.
5. **Deprecated carriers:** `TIP_CAR_480_A00` / `PLT_CAR_L5AC_A00` warn; the new names are
   `hamilton_tip_carrier_L5` / `hamilton_plate_carrier_L5_ac`.
6. **Realistic motion time:** `STAR(simulation=True, driver=STARSimulationDriver(simulate_motion_time=True,
   motion_time_scale=...))` makes the simulator sleep for modelled move times, a more honest
   alternative to hand-placed sleeps (mind should-fix 6).
7. **Kinetic sample time:** for the microsomal-stability story the relevant time is when the
   quench aspiration happened. Have the scheduler timestamp the `aspirate`/`dispense` intermediate
   steps (when received) and report actual sample times vs nominal in `run_summary.md`.
8. **Workflow detail:** StartShaking (step 5) is followed immediately by the t=0 StopShaking, so
   the first shake lasts milliseconds; either skip step 5 or start shaking after the t=0 sample.

## Phase 2: code

### Round 1 (04:47-04:55 UTC)

Status of the Phase 1 items: blockers 1 (deep-well plates), 2 (`_log_exchange` hook), 4 (wait for
`done`, best-effort intermediates) are handled in the code; blocker 3 is handled differently
(see S1 below). Should-fix 1, 2, 3, 4, 5, 7, 9 (mostly), 11 (LH) are done.

Tests run by the reviewer:
- `tests/test_hhs_twin.py`: **6/6 pass** (ramp 22 -> 36.51 C in 10.3 s, 42 intermediates; both
  defined errors via dynamic and generated client; exit 0 on SIGTERM).
- `tests/test_lh_twin.py`: **all checks pass** (NotInitialized, LiquidHandlingError for unknown
  plate / too little liquid / out of tips, 39 Status updates, exit 0).
- Reviewer probes (free ports, all servers killed): Transfer = 0.83-0.93 s with motion scale 0.1,
  4/4 Step intermediates received, ~100 firmware commands per Transfer.

#### Found and already fixed by the builder

- **B-fixed. LH server did not exit on SIGTERM** (reproduced at 04:49: still alive 20 s after
  SIGTERM, had to be killed). Cause: `Transfer_default_lifetime_of_execution = timedelta(minutes=30)`;
  sila2 0.14 then starts a non-daemon thread per finished instance that sleeps out the lifetime
  (`observable_command_manager.py`, `remove_command_manager_from_servicer`), blocking interpreter
  exit for up to 30 min. Now `None` (`liquidhandlerservice_impl.py:81`); re-tested: exit in 0.2 s.
  Keep it that way and keep the comment: it is a good teaching note.

#### Should-fix

- **S1. Scheduler: record status and t0 in one critical section** (`scheduler/scheduler.py:257-258`
  vs `:198-205`). `_execute` sets `rec.status = "succeeded"` *outside* `self._cond`, and t0 is set
  later under the lock. A lane that re-evaluates in between (its `_cond.wait(timeout=...)` for a
  timed step expires) can see the t0 step succeeded with `self.t0_s is None` and crash on
  `self.t0_s + ...` (`:229`, TypeError kills that lane thread, run hangs on `join`). Not reachable
  with today's YAML (no timed step is pending-with-deps-met before t0), but it contradicts the
  comment "guards records/t0/failed". *Fix:* have `_execute` return `(status, responses, error)`
  and write status, end time and t0 in the locked block in `_lane`; or guard `:229` with
  `if self.t0_s is None: continue`.
  Note on Phase 1 blocker 3(c): the lane picks the *first runnable* step, not strict FIFO, so the
  lane-order deadlock cannot happen; explicit-dependency cycle check (`workflow.py:108-124`) plus
  "timed steps must depend on the t0 step" and the global `failed` flag cover the rest. Good design;
  worth one sentence in the docs that lanes may run steps out of file order.

- **S2. Unobservable SiLA calls have no deadline** (`scheduler.py:254`). A hung server blocks the
  lane forever (gRPC has no default timeout); `result_timeout_s` only covers observable results.
  *Fix (cheap):* run the whole step with a watchdog, or at least document it; the run_demo
  `finally` will kill servers, which then unblocks the call with an RpcError.

- **S3 (high). Two servers can share a port, and nothing notices.** *Verified:* gRPC Python sets
  `SO_REUSEPORT`, so a second `python -m lh_twin --port P` starts happily next to a running one,
  and the kernel spreads connections over both (12 connections -> 2 distinct `ServerUUID`s).
  sila2's `SilaServer` builds `grpc.server(...)` without options, so this can't be switched off
  from the impl. Default ports are fixed (50052/50053), and `tests/test_smoke.py:223` hard-codes
  50062/50063, so a leftover server from a crashed run, or a test running alongside a demo (this
  happened during review: three agents running demos/tests at once), silently mixes two twins'
  state: a Transfer may go to one STAR and `GetWellVolumes` to the other. *Fix:* in
  `run_demo.py` before `Popen`, bind-test the port with a plain socket (no `SO_REUSEPORT`, so it
  fails with `EADDRINUSE` if any server listens; do set `SO_REUSEADDR`, so leftover TIME_WAIT
  connections from the previous run don't cause a false alarm) and stop with a clear message; additionally pass
  `--server-uuid <uuid4>` to each server and check `client.SiLAService.ServerUUID.get()` in
  `wait_for_server`. In `test_smoke.py`, use `free_port()` like the twin tests do.

- **S4. Server log file handles leak** (`run_demo.py:39`): `log_path.open("w")` is never closed.
  Keep the handle with the proc (e.g. return `(proc, fp)`) and close it in `stop_server`.

- **S5. LH `shutdown()` doesn't take the op lock or join the loop thread**
  (`twin.py:402-410`). `star.stop()` can run concurrently with a Transfer in progress, and the loop
  is stopped but never closed. Low impact (process exits anyway), but for a teaching POC:
  `with self._op_lock:` around it, then `self._loop_thread.join(timeout=5); self._loop.close()`.

#### Nice-to-have

- **N1. Initial `Status` "idle" before Initialize** (`liquidhandlerservice_impl.py` `__init__`):
  "not initialized" would be more honest and matches `NotInitialized`.
- **N2. HHS periodic tick swallows exceptions** (`heatershakerservice_impl.py:98`,
  `run_periodically`): an exception in `_tick` silently kills the loop (the Future is never read),
  and `CurrentTemperature` stops updating. Wrap the body in `try/except Exception: logger.exception`.
- **N3. Superseded SetTemperature raises `UndefinedExecutionError`** (`heatershakerservice_impl.py:210`)
  - correct given the FDL; mention in docs that a `SetpointChanged` defined error would be the
  cleaner v1.1 FDL change.
- **N4. Duplicated contract values:** `scheduler/report.py:26-28` repeats plate names and start
  volumes from `twin.py:91-96`. Fine for a POC; could read them from `GetDeckLayout`'s
  `poc_layout` instead.
- **N5. t0 semantics:** t0 = end of the NADPH Transfer (after the tip drop), ~0.2 s after the
  actual dispense. Either say so in the summary or take t0 from the time the `3/4 dispense`
  intermediate arrived.

### Round 2 (04:55-05:00 UTC): end to end

- `tests/test_smoke.py`: **4/4 pass** (fake-client dependency/timing run, fake failure drains the
  run, validation rejects cycles and untimed t0, real end-to-end demo in 31 s).
- Builder's `run_demo.py` output in `results/` checked: 27/27 steps succeeded in 32 s; timed
  StopShaking steps started 0.00 s late; heat 22 -> 36.51 C and cool 37 -> 22.49 C in 10.3 s each;
  final volumes match the expected ones exactly (compounds/nadph col 1 150, reaction col 1 150,
  quench cols 1-5 200 uL); 863 firmware commands traced. `run_summary.md` explains effective vs
  nominal sample time well.
- No new blockers. Open items, in order: **S3** (shared ports via SO_REUSEPORT), S1 (status/t0
  race), S4 (log handles), S2/S5, then the nice-to-haves.

### Verdict

The three parts run together and the tests pass. The design holds up for a teaching POC:
twin/SiLA separation in the LH server (`twin.py` knows PLR, the impl knows SiLA), analytic
thermal model with generation counter in the HHS twin, and a scheduler whose "first runnable step
per lane" rule plus validation avoids the deadlocks the plan risked.
