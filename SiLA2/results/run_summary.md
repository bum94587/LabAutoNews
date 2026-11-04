# Run summary: SiLA 2 digital-twin POC

- Workflow: **mini microsomal stability (1 compound, 5 time points)**
- Result: **SUCCEEDED**: 27 succeeded
- Started 2026-11-04T04:50:47.936+00:00 (UTC), real duration 32.15 s
- Time scale: 1 workflow minute = 2 s real; t0 (NADPH added) at 11.06 s after run start
- Liquid handler: Model: Hamilton Microlab STAR (digital twin, no hardware). Driver: PyLabRobot v1 pylabrobot.hamilton.star.STAR, commit 7779f506d12755f5f274b4c5cab4d095f4fccb62. Simulator: STARSimulationDriver - firmware-level; assembles the real firmware command strings and answers reads from PLR's resource/volume model, configured from a recorded real STAR (star_legacy_2021_8ch_head96_autoload1D: 8 x 1000 uL channels, 96-head, iSWAP, autoload). Motion time scale: 0.1 (1 = real speed, 0 = instant). Labware: hamilton_tip_carrier_L5 + hamilton_96_tiprack_300uL_filter; hamilton_plate_carrier_L5_ac + 4 x cor_96_wellplate_2mL_Vb deep-well plates (deep wells because reaction reaches 400 uL); compounds=200 uL/well, nadph=200 uL/well, reaction=300 uL/well, quench=150 uL/well.
[Hamilton STAR] Connected on simulation (no link)
  Firmware: master 7.6S 25 2021_11_05 (GRU C0), pipettes 4.0S j 2022-03-16, x_arm 1.4S 2012-04-25, head96 5.0S i 2021-10-22 (H0 XE167), iswap 4.1S 2011-12-19, autoload 3.4S f 2017-01-09
  Arms: 1
  Configuration: 54 slots
  Autoload: 1D barcode scanner
    left: hamilton_legacy_star_dual_rail_arm, 354.0 mm wide, travel 95.0 to 1340.2 mm, workspace -323.2 to 1517.2 mm
      channels: 8 (1000uL) | 96-head: 96 head II | 384-head: none | iSWAP: wide gripper

## Steps

| step | device | command | start (s) | duration (s) | late (s) | status | intermediates | result |
|---|---|---|---:|---:|---:|---|---:|---|
| heat_to_37 | hhs | SetTemperature | 0.00 | 10.28 | - | succeeded | 42 | ReachedTemperature=36.51 |
| lh_init | lh | Initialize | 0.00 | 0.21 | - | succeeded | 0 | Summary=STAR twin initialised: 148 firmware commands exchanged with the simul... |
| add_compound | lh | Transfer | 0.21 | 0.91 | - | succeeded | 4 | Message=Transfer 50 uL compounds col 1 -> reaction col 1: done (pick up tips:... |
| add_nadph | lh | Transfer | 10.28 | 0.78 | - | succeeded | 4 | Message=Transfer 50 uL nadph col 1 -> reaction col 1: done (pick up tips: tip... |
| shake_start | hhs | StartShaking | 11.06 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_t0 | hhs | StopShaking | 11.06 | 0.00 | 0.00 | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| sample_t0 | lh | Transfer | 11.07 | 0.86 | - | succeeded | 4 | Message=Transfer 50 uL reaction col 1 -> quench col 1: done (pick up tips: ti... |
| shake_t0 | hhs | StartShaking | 11.93 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_t1 | hhs | StopShaking | 13.06 | 0.00 | 0.00 | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| sample_t1 | lh | Transfer | 13.06 | 0.82 | - | succeeded | 4 | Message=Transfer 50 uL reaction col 1 -> quench col 2: done (pick up tips: ti... |
| shake_t1 | hhs | StartShaking | 13.89 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_t2 | hhs | StopShaking | 15.06 | 0.00 | 0.00 | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| sample_t2 | lh | Transfer | 15.06 | 0.82 | - | succeeded | 4 | Message=Transfer 50 uL reaction col 1 -> quench col 3: done (pick up tips: ti... |
| shake_t2 | hhs | StartShaking | 15.88 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_t3 | hhs | StopShaking | 17.06 | 0.00 | 0.00 | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| sample_t3 | lh | Transfer | 17.07 | 0.85 | - | succeeded | 4 | Message=Transfer 50 uL reaction col 1 -> quench col 4: done (pick up tips: ti... |
| shake_t3 | hhs | StartShaking | 17.92 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_t5 | hhs | StopShaking | 21.06 | 0.00 | 0.00 | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| sample_t5 | lh | Transfer | 21.06 | 0.80 | - | succeeded | 4 | Message=Transfer 50 uL reaction col 1 -> quench col 5: done (pick up tips: ti... |
| shake_t5 | hhs | StartShaking | 21.87 | 0.00 | - | succeeded | 0 | Message=Shaking at 600 rpm (was 0 rpm) |
| stop_final | hhs | StopShaking | 21.87 | 0.00 | - | succeeded | 0 | Message=Shaking stopped (was 600 rpm) |
| cool_to_22 | hhs | SetTemperature | 21.87 | 10.28 | - | succeeded | 42 | ReachedTemperature=22.49 |
| volumes_compounds | lh | GetWellVolumes | 21.87 | 0.00 | - | succeeded | 0 | VolumesJson={"A1": 150.0, "A2": 200.0, "A3": 200.0, "A4": 200.0, "A5": 200.0,... |
| volumes_nadph | lh | GetWellVolumes | 21.87 | 0.00 | - | succeeded | 0 | VolumesJson={"A1": 150.0, "A2": 200.0, "A3": 200.0, "A4": 200.0, "A5": 200.0,... |
| volumes_reaction | lh | GetWellVolumes | 21.87 | 0.00 | - | succeeded | 0 | VolumesJson={"A1": 150.0, "A2": 300.0, "A3": 300.0, "A4": 300.0, "A5": 300.0,... |
| volumes_quench | lh | GetWellVolumes | 21.88 | 0.00 | - | succeeded | 0 | VolumesJson={"A1": 200.0, "A2": 200.0, "A3": 200.0, "A4": 200.0, "A5": 200.0,... |
| firmware_trace | lh | GetFirmwareTrace | 21.88 | 0.01 | - | succeeded | 0 | TraceJson=[{"index": 0, "time": "2026-11-04T04:50:48.002+00:00", "command": "... |

## Time points

| sample | nominal (min) | due (s) | stop-shake late (s) | quenched at (min after t0) | status |
|---|---:|---:|---:|---:|---|
| sample_t0 -> quench col 1 | 0.0 | 11.06 | 0.00 | 0.43 | succeeded |
| sample_t1 -> quench col 2 | 1.0 | 13.06 | 0.00 | 1.41 | succeeded |
| sample_t2 -> quench col 3 | 2.0 | 15.06 | 0.00 | 2.41 | succeeded |
| sample_t3 -> quench col 4 | 3.0 | 17.06 | 0.00 | 3.43 | succeeded |
| sample_t5 -> quench col 5 | 5.0 | 21.06 | 0.00 | 5.40 | succeeded |

Effective time = end of the sampling Transfer (aliquot dispensed into acetonitrile). The gap to nominal is the Transfer's own duration in workflow minutes; a real method would start each sampling step early by that amount.

## Temperatures (heater-shaker twin)

- `heat_to_37`: target 37.0 C, from 22.0 C reached 36.51 C in 10.28 s real (42 CurrentTemperature updates); status succeeded
- `cool_to_22`: target 22.0 C, from 37.0 C reached 22.49 C in 10.28 s real (42 CurrentTemperature updates); status succeeded

## Firmware trace (simulated Hamilton STAR)

863 firmware commands were sent to the STAR simulator. Most frequent:

| code | count | meaning |
|---|---:|---|
| `C0RY` | 58 |  |
| `P1RZ` | 44 |  |
| `P2RZ` | 44 |  |
| `P3RZ` | 44 |  |
| `P4RZ` | 44 |  |
| `P5RZ` | 44 |  |
| `P6RZ` | 44 |  |
| `P7RZ` | 44 |  |
| `P8RZ` | 44 |  |
| `P1RD` | 29 |  |
| `P2RD` | 29 |  |
| `P3RD` | 29 |  |

Example (first aspirate, or first command):

```
> C0ASat0 0 0 0 0 0 0 0tm1 1 1 1 1 1 1 1xp02526 02526 02526 02526 02526 02526 02526 02526yp1455 1365 1275 1185 1095 1005 0915 0825th2450te2450lp2302 2302 2302 2302 2302 2302 2302 2302ch000 000 000 000 000 000 000 000zl1874 1874 1874 1874 1874 1874 1874 1874po0100 0100 0100 0100 0100 0100 0100 0100zu0032 0032 0032 0032 0032 0032 0032 0032zr06180 06180 06180 06180 06180 06180 06180 06180zx1874 1874 1874 1874 1874 1874 1874 1874ip0000 0000 0000 0000 0000 0000 0000 0000it0 0 0 0 0 0 0 0fp0000 0000 0000 0000 0000 0000 0000 0000av00551 00551 00551 00551 00551 00551 00551 00551as1000 1000 1000 1000 1000 1000 1000 1000ta000 000 000 000 000 000 000 000ba0000 0000 0000 0000 0000 0000 0000 0000oa050 050 050 050 050 050 050 050lm0 0 0 0 0 0 0 0ll1 1 1 1 1 1 1 1lv1 1 1 1 1 1 1 1zo000 000 000 000 000 000 000 000ld00 00 00 00 00 00 00 00de0020 0020 0020 0020 0020 0020 0020 0020wt10 10 10 10 10 10 10 10mv00000 00000 00000 00000 00000 00000 00000 00000mc00 00 00 00 00 00 00 00mp000 000 000 000 000 000 000 000ms1000 1000 1000 1000 1000 1000 1000 1000mh0000 0000 0000 0000 0000 0000 0000 0000gi000 000 000 000 000 000 000 000gj0gk0lk0 0 0 0 0 0 0 0ik0000 0000 0000 0000 0000 0000 0000 0000sd0500 0500 0500 0500 0500 0500 0500 0500se0500 0500 0500 0500 0500 0500 0500 0500sz0300 0300 0300 0300 0300 0300 0300 0300io0000 0000 0000 0000 0000 0000 0000 0000
< None
```

## Final volumes (column means, uL)

| plate | column | twin | expected from workflow + PLAN start volumes |
|---|---:|---:|---:|
| compounds | 1 | 150.0 | 150.0 |
| nadph | 1 | 150.0 | 150.0 |
| reaction | 1 | 150.0 | 150.0 |
| quench | 1 | 200.0 | 200.0 |
| quench | 2 | 200.0 | 200.0 |
| quench | 3 | 200.0 | 200.0 |
| quench | 4 | 200.0 | 200.0 |
| quench | 5 | 200.0 | 200.0 |

Columns not listed were not touched by the workflow.

## Files

- `timeline.json`: every step with start/end, status, responses and intermediate responses
- `firmware_trace.json`: Hamilton firmware command strings sent to the simulated STAR, with replies
- `well_volumes.json`: tracked volume of every well of the four plates
- `gantt.svg`, `plate_volumes.svg`: plots of the above
- `run_log.txt`: scheduler live log; `logs/lh_twin.log`, `logs/hhs_twin.log`: server output
