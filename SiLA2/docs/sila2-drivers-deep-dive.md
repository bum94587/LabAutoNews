# Deep dive: SiLA 2 drivers in Python, and who actually ships one for a liquid handler, 3 Nov 2026

Scope: what SiLA 2 is, the state of its Python tooling, which liquid handlers have a SiLA 2 interface (vendor, third-party or community), and what that means for a DMPK lab. Companion to the digital-twin POC in this folder ([README](../README.md)). sila-standard.com and unitelabs.io were blocked here, so claims from those sites rest on search snippets and are marked; everything tagged "code" was read from a git clone.

Verifier (independent agent, 3 Nov): 7 items verified, 3 partly verified, none contradicted; corrections applied (EVOware attribution, Opentrons wording, dates). Badges: ✅ verified · 🟡 partly verified · 🔬 sound.

## TL;DR

- **SiLA 2 standardises the plumbing, not the pipetting.** It defines discovery, gRPC transport, observable commands, errors, locking and simulation, but the official feature library still has **no standard liquid-handling feature**, so every liquid-handler server invents its own commands [1][2]. ✅🔬
- **The official Python SDK (`sila2`) was marked "Unmaintained" on 17 Sep 2026** and points users to UniteLabs' `unitelabs-sila` (0.14.0, 2 Nov 2026); its last release is 0.14.0 from 1 Dec 2025 [3][4]. ✅
- **Vendor-shipped SiLA 2 for liquid handlers is rare.** Tecan has published an open-source FluentControl SiLA 2 connector since 2020 and Dispendix's I.DOT has a native server; we found **no vendor-published Hamilton, Beckman Biomek or Opentrons SiLA 2 interface** (community Opentrons connectors exist) [5][6][7]. 🟡
- **For a Hamilton STAR, the realistic open route today is a twin or driver you wrap yourself**, which is what this folder's POC does with PyLabRobot's firmware-level STAR simulator behind a SiLA 2 server [8].

## SiLA 2 in five minutes

**What it is.** SiLA (Standardization in Lab Automation) is a non-profit consortium; SiLA 2 is its vendor-neutral interface standard for lab devices and software, succeeding the SOAP-based SiLA 1 [1]. The standard's GitLab group holds the schema, the protocol definitions and a feature library; release tags are v1.0 (1 Oct 2019), v1.1 (17 Mar 2022) and a new **v1.2 "Official Release 1.2" tagged 5 Feb 2026**, though no v1.2 specification document has been published and the public Parts A/B still read v1.1 [1]. ✅

**The moving parts**, as implemented in code [1][3]:

| Term | What it means in practice |
|---|---|
| **Feature** | An XML file (Feature Definition Language, `*.sila.xml`) listing commands, properties, errors and data types, validated against `FeatureDefinition.xsd` |
| **Server** | A program exposing one or more features (colloquially "the driver"); every server must implement the `SiLAService` core feature |
| **Client** | A scheduler, LIMS, script or UI that calls a server |
| **Unobservable command** | Returns once, like a normal function call |
| **Observable command** | Long-running: returns an execution id, then streams progress, intermediate responses and a final result (a pipetting run, an incubation) |
| **Observable property** | A subscription stream, such as the current temperature |
| **Defined execution error** | A named, documented failure the client can handle (for example `TemperatureOutOfRange`) |

Transport is gRPC over HTTP/2 with Protocol Buffers; servers advertise themselves by mDNS as `_sila._tcp.local.` [1][3]. TLS is mandatory in the specification; the Python SDK's unencrypted mode is documented as violating the spec and meant for testing [3]. Version 1.1 added a server-initiated ("cloud") mode, which the `sila2` Python SDK does not support [3].

## The feature library: generic, with a gap where pipetting should be

The core features cover plumbing every device needs: `SiLAService` (mandatory), `LockController`, `SimulationController`, `CancelController`, `PauseController`, `ErrorRecoveryService`, authentication, and the server-initiated `ConnectionConfigurationService` [2]. For instruments there are two Verified features for handing a plate between a robot arm and a device (`LabwareTransferManipulatorController`, `LabwareTransferSiteController`) and a draft `CoverController` [2].

There is **no** standard `LiquidHandler`, aspirate/dispense, deck, labware or tip feature [2]. *Analysis:* a client written against Tecan's Fluent server will not drive any other liquid handler; "SiLA 2-enabled liquid handler" today usually means "start a named vendor method remotely".

## Python tooling: the centre of gravity moved

| Package | Status | Notes |
|---|---|---|
| `sila2` (official, gitlab.com/SiLA2/sila_python) | 0.14.0, 1 Dec 2025; **marked Unmaintained 17 Sep 2026** | XML-first: write the feature file, generate a package with `sila2-codegen new-package`, implement the generated base class. No server-initiated mode [3] |
| `unitelabs-sila` (UniteLabs) | 0.14.0, 2 Nov 2026 | An "unopinionated" async library; "SiLA 2 1.1 compliant", includes a cloud server class [4] |
| `unitelabs-cdk` (UniteLabs) | 0.17.1, 22 Oct 2026 | Code-first connector framework on top; the base for several community connectors, such as the Acceleration Consortium's Opentrons ones [4][12] |
| SiLA Rust | 0.1.0 on crates.io, 3 Nov 2026 | Reports full interop with the Python test client and server (349/349 and 104/104 checks, self-reported) [9] ✅ |
| C#/.NET (`SiLA2.Core`), Tecan SDK (`Tecan.Sila2`) | 10.3.3 (6 Oct 2026); 4.4.8 (NuGet, 30 Sep 2026) | Actively released .NET options [9] |

*Why this POC still uses `sila2`:* its codegen route makes the feature-file → base-class model explicit, which is the point of a teaching demo. New production work should start on the UniteLabs libraries (*analysis*).

## Liquid handlers: who ships what

| Instrument | SiLA 2 interface | Who provides it |
|---|---|---|
| **Tecan Fluent** | Open-source FluentControl connector (C#/.NET server plus a Python client): start Fluent or its simulation mode, run and pause methods, set variables, plus worklist-style aspirate/dispense; BSD-3, published 2020, updated Oct 2025 | **Vendor** [5] 🟡🔬 |
| Tecan Fluent | UniteLabs FluentControl connector (VisionX COM API), v0.5.1 | Third party [4] |
| Tecan Freedom EVO | "Tecan EVOware driver (SiLA 2)" listed in SiLA's device directory, v1.0 (Nov 2024), needs EVOware Plus 2.7 (snippet) | Third party (UniteLabs), listed [10] |
| **Dispendix I.DOT** | Native SiLA 2 server on the instrument (client-initiated connections, mDNS); C# client samples since 2022 | **Vendor** [6] 🟡🔬 |
| **Hamilton STAR / VANTAGE** | No Hamilton-published SiLA 2 server found. UniteLabs says it sells STAR and VANTAGE connectors (vendor-stated, not in its public repos). SiLA's directory lists a driver for Hamilton's Zeus OEM pipetting channel, probably SiLA 1-style (snippet) | Third party, commercial (unverified) [7] 🟡 |
| **Beckman Biomek** | None found; Biomek's integration module "SILAS" is not SiLA | — [7] |
| Beckman/Labcyte **Echo** 5xx | Community Python `sila2` server (Uppsala) with a C# helper service, in active use as of Aug 2025 (README) | Community [11] |
| **Opentrons OT-2 / Flex** | Community connectors on the UniteLabs CDK (Acceleration Consortium), including a full simulator for the Flex | Community [12] |
| Agilent Bravo | VWorks installs a "SiLA XMLRPC Server" for the ODTC, which looks SiLA 1-style; no native SiLA 2 found | — (snippet) [7] |

Schedulers: we found no documented SiLA 2 support in Biosero Green Button Go, HighRes Cellario, Thermo Momentum or Genedata Screener, although HighRes has joined the SiLA consortium (older, undated announcement; snippet) [13].

## Where PyLabRobot fits

PyLabRobot drives liquid handlers directly through firmware or vendor APIs, not through SiLA. It uses SiLA only to reach devices that already have a server: it can discover SiLA 1 and SiLA 2 devices on the network, talks raw gRPC to Molecular Devices' ImageXpress Pico, and uses INHECO's SiLA 1 SOAP flavour for INHECO devices (ODTC, SCILA) [8]. ✅🔬 *Analysis:* the two approaches compose. PyLabRobot can supply the device-level control, and a thin SiLA 2 server on top (as in this POC) makes that control callable from any SiLA client or scheduler.

## Also new this autumn

- **OPC UA LADS**, the other open device standard, got official .NET SDK packages (server, client, sample) merged on 1 Nov 2026; LADS Part 1 v1.0.0 dates from November 2023, and its supplier list appears to show no liquid handlers (unverified snippet) [14]. ✅
- SiLA published a "Letter of Intent on Open Standards for Life Sciences" on 6 Jul 2026 naming both SiLA 2 and LADS (snippet), and started an **AI working group** in January 2026 (snippet) [10].
- Agent bridges exist: K-Dense's `labmcp-sila2` lets an AI agent call any SiLA 2 server, but describes itself as "simulated", tested only against an in-process `sila2` server [15]. ✅🔬

## What to watch

- **A standard liquid-handling feature** in the SiLA library, which would be the first step toward portable aspirate/dispense across vendors [2].
- **Hamilton's position**: whether Hamilton or its integrators publish an open SiLA 2 interface, and whether UniteLabs' STAR connector becomes public [7].
- **Python migration**: how fast tools built on `sila2` (including agent bridges) move to `unitelabs-sila` [3][4][15].

## References

1. SiLA 2 base repository (schema, protocol definitions, feature library; tags v1.0/v1.1/v1.2): [https://gitlab.com/SiLA2/sila_base](https://gitlab.com/SiLA2/sila_base) (code); SiLA 2 overview paper, *SLAS Technology* (2022): [https://pubmed.ncbi.nlm.nih.gov/35639108/](https://pubmed.ncbi.nlm.nih.gov/35639108/) (paper)
2. SiLA feature library, `feature_definitions/` in sila_base (e.g. `org/silastandard/core/`, `org/silastandard/instruments/`): [https://gitlab.com/SiLA2/sila_base/-/tree/master/feature_definitions](https://gitlab.com/SiLA2/sila_base/-/tree/master/feature_definitions) (code)
3. `sila_python` README ("Project Status: Unmaintained", commit of 17 Sep 2026) and docs: [https://gitlab.com/SiLA2/sila_python](https://gitlab.com/SiLA2/sila_python) (code); PyPI `sila2`: [https://pypi.org/project/sila2/](https://pypi.org/project/sila2/) (primary)
4. UniteLabs `unitelabs-sila`: [https://pypi.org/project/unitelabs-sila/](https://pypi.org/project/unitelabs-sila/), source [https://gitlab.com/unitelabs/sila2/sila-python](https://gitlab.com/unitelabs/sila2/sila-python); `unitelabs-cdk`: [https://gitlab.com/unitelabs/cdk/python-cdk](https://gitlab.com/unitelabs/cdk/python-cdk); FluentControl connector: [https://gitlab.com/unitelabs/connectors/tecan-fluentcontrol](https://gitlab.com/unitelabs/connectors/tecan-fluentcontrol) (code / primary)
5. Tecan Fluent SiLA 2 connector: [https://gitlab.com/tecan/fluent-sila2-connector](https://gitlab.com/tecan/fluent-sila2-connector) (code)
6. Dispendix I.DOT SiLA 2 samples: [https://github.com/Dispendix/dx-idot-sila2-samples](https://github.com/Dispendix/dx-idot-sila2-samples) (code)
7. Searches of Hamilton, Beckman, Agilent and SiLA listings (no public SiLA 2 interface found); UniteLabs liquid-handling page (vendor-stated): [https://unitelabs.io/lab-automation-solutions/liquid-handling/](https://unitelabs.io/lab-automation-solutions/liquid-handling/); UniteLabs public GitLab group (no Hamilton connector): [https://gitlab.com/unitelabs](https://gitlab.com/unitelabs) (snippet / primary)
8. PyLabRobot SiLA discovery and gRPC helpers at commit 7779f50: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/discovery.py](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/discovery.py), [grpc.py](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/grpc.py) (code)
9. SiLA Rust: [https://gitlab.com/SiLA2/sila_rust](https://gitlab.com/SiLA2/sila_rust); SiLA C#: [https://gitlab.com/SiLA2/sila_csharp](https://gitlab.com/SiLA2/sila_csharp); Tecan SiLA2 SDK: [https://gitlab.com/SiLA2/vendors/sila_tecan](https://gitlab.com/SiLA2/vendors/sila_tecan) (code / primary)
10. SiLA device directory entry, Tecan EVOware driver (SiLA 2): [https://sila-standard.com/sila_device/tecan-evoware-driver-sila-2/](https://sila-standard.com/sila_device/tecan-evoware-driver-sila-2/); Letter of Intent on Open Standards: [https://sila-standard.com/letter-of-intent-on-open-standards-for-life-sciences/](https://sila-standard.com/letter-of-intent-on-open-standards-for-life-sciences/); AI working group: [https://sila-standard.com/we-are-excited-to-announce-a-new-sila-working-group-on-ai/](https://sila-standard.com/we-are-excited-to-announce-a-new-sila-working-group-on-ai/) (snippet)
11. Echo SiLA 2 server (Uppsala): [https://gitlab.com/OpenLabAutomation/device-integration/echo](https://gitlab.com/OpenLabAutomation/device-integration/echo) (code)
12. Acceleration Consortium Opentrons connectors: [https://github.com/AccelerationConsortium/opentrons-flex](https://github.com/AccelerationConsortium/opentrons-flex), [https://github.com/AccelerationConsortium/opentrons-ot2](https://github.com/AccelerationConsortium/opentrons-ot2) (code)
13. HighRes joins SiLA: [https://www.highresbio.com/news/highres-biosolutions-joins-sila](https://www.highresbio.com/news/highres-biosolutions-joins-sila) (snippet)
14. OPC Foundation UA-.NETStandard PR #4945 (LADS 1.0.0 packages): [https://github.com/OPCFoundation/UA-.NETStandard/pull/4945](https://github.com/OPCFoundation/UA-.NETStandard/pull/4945) (primary)
15. K-Dense `labmcp-sila2`: [https://github.com/K-Dense-AI/lab-instrument-mcps/tree/46545ea7eb818249a524c3340dc80657f448430f/servers/protocols/sila2](https://github.com/K-Dense-AI/lab-instrument-mcps/tree/46545ea7eb818249a524c3340dc80657f448430f/servers/protocols/sila2) (code)

> **Rate:** _/5 · **Tags:** _ · `LAN-F20261103`
