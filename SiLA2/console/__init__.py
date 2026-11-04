"""Operator console for the SiLA 2 twin POC: run, watch and poke the twin servers.

* ``console.ctl``: a command-line control (``python -m console.ctl ...``) that prints JSON. It
  starts and stops the two twin servers in the background, introspects and calls their SiLA
  features, lists and runs methods (workflow YAML files), and reports status. The myday viewer
  drives the twin through it, but it is just as usable from a shell.
* ``console.traffic``: a gRPC server interceptor that records every SiLA call a twin server
  handles as JSON lines, so the SiLA traffic can be watched live.
* ``console.paths``: where the runtime state lives (``runtime/``, git-ignored).

Nothing here changes how the POC behaves when it is not used: ``run_demo.py`` and the tests
start the servers without it.
"""
