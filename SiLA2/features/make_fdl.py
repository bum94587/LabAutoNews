"""Generate the two SiLA 2 Feature Definition (FDL) files used by this POC.

Run: uv run python features/make_fdl.py   (rewrites features/*.sila.xml)
"""
from pathlib import Path
from xml.sax.saxutils import escape

HEAD = ('<Feature xmlns="http://www.sila-standard.org" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'Category="{cat}" FeatureVersion="1.0" MaturityLevel="Draft" Originator="org.labautonews" SiLA2Version="1.0" '
        'xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">')

def el(tag, ident, display, desc, inner=""):
    return f"<{tag}><Identifier>{ident}</Identifier><DisplayName>{escape(display)}</DisplayName><Description>{escape(desc)}</Description>{inner}</{tag}>"

def dt(basic): return f"<DataType><Basic>{basic}</Basic></DataType>"

def param(i, d, desc, basic): return el("Parameter", i, d, desc, dt(basic))
def resp(i, d, desc, basic): return el("Response", i, d, desc, dt(basic))
def inter(i, d, desc, basic): return el("IntermediateResponse", i, d, desc, dt(basic))

def command(i, d, desc, params=(), responses=(), intermediate=(), observable=False, errors=()):
    inner = f"<Observable>{'Yes' if observable else 'No'}</Observable>" + "".join(params) + "".join(responses) + "".join(intermediate)
    if errors:
        inner += "<DefinedExecutionErrors>" + "".join(f"<Identifier>{e}</Identifier>" for e in errors) + "</DefinedExecutionErrors>"
    return el("Command", i, d, desc, inner)

def prop(i, d, desc, basic, observable=False, errors=()):
    inner = f"<Observable>{'Yes' if observable else 'No'}</Observable>" + dt(basic)
    if errors:
        inner += "<DefinedExecutionErrors>" + "".join(f"<Identifier>{e}</Identifier>" for e in errors) + "</DefinedExecutionErrors>"
    return el("Property", i, d, desc, inner)

def error(i, d, desc): return el("DefinedExecutionError", i, d, desc)

def feature(cat, ident, display, desc, items):
    return HEAD.format(cat=cat) + f"<Identifier>{ident}</Identifier><DisplayName>{escape(display)}</DisplayName><Description>{escape(desc)}</Description>" + "".join(items) + "</Feature>\n"

ERR = ("NotInitialized", "LiquidHandlingError")
MSG = resp("Message", "Message", "Human-readable summary of what the digital twin did", "String")
LH = feature("liquidhandling", "LiquidHandlerService", "Liquid Handler Service",
  "Column-wise (8-channel) liquid handling on a Hamilton STAR digital twin: PyLabRobot's v1 STAR firmware-level simulator plus its resource and volume model.", [
  command("Initialize", "Initialize", "Set up the STAR twin: run firmware discovery and initialisation against the simulator and load the POC deck layout.",
          responses=[resp("Summary", "Summary", "Instrument and deck summary", "String")]),
  command("GetDeckLayout", "Get Deck Layout", "Return the deck as JSON: carriers, plates, tip racks and their locations.",
          responses=[resp("DeckLayoutJson", "Deck Layout JSON", "Deck tree as JSON", "String")], errors=ERR[:1]),
  command("PickUpTips", "Pick Up Tips", "Pick up 8 tips from one column of a tip rack.",
          params=[param("TipRack", "Tip Rack", "Tip rack resource name", "String"), param("Column", "Column", "Column number, 1-12", "Integer")],
          responses=[MSG], errors=ERR),
  command("Aspirate", "Aspirate", "Aspirate the same volume with 8 channels from one plate column.",
          params=[param("Plate", "Plate", "Plate resource name", "String"), param("Column", "Column", "Column number, 1-12", "Integer"),
                  param("VolumeUl", "Volume (uL)", "Volume per channel in microlitres", "Real")],
          responses=[MSG], errors=ERR),
  command("Dispense", "Dispense", "Dispense the same volume with 8 channels into one plate column.",
          params=[param("Plate", "Plate", "Plate resource name", "String"), param("Column", "Column", "Column number, 1-12", "Integer"),
                  param("VolumeUl", "Volume (uL)", "Volume per channel in microlitres", "Real")],
          responses=[MSG], errors=ERR),
  command("DropTips", "Drop Tips", "Return the mounted tips to the spots they came from.", responses=[MSG], errors=ERR),
  command("Transfer", "Transfer", "Pick up fresh tips, aspirate from a source column, dispense into a target column, drop tips. Observable: reports each step.",
          params=[param("SourcePlate", "Source Plate", "Source plate name", "String"), param("SourceColumn", "Source Column", "1-12", "Integer"),
                  param("TargetPlate", "Target Plate", "Target plate name", "String"), param("TargetColumn", "Target Column", "1-12", "Integer"),
                  param("VolumeUl", "Volume (uL)", "Volume per channel in microlitres", "Real")],
          responses=[MSG], intermediate=[inter("Step", "Step", "The sub-step now running", "String")], observable=True, errors=ERR),
  command("GetWellVolumes", "Get Well Volumes", "Return the twin's tracked volume (uL) of every well of a plate, as JSON {well: volume}.",
          params=[param("Plate", "Plate", "Plate resource name", "String")],
          responses=[resp("VolumesJson", "Volumes JSON", "Well volumes as JSON", "String")], errors=ERR),
  command("GetFirmwareTrace", "Get Firmware Trace", "Return Hamilton firmware command strings the twin has sent to the simulated instrument, from an index on, as JSON list.",
          params=[param("SinceIndex", "Since Index", "First trace index to return (0 = all)", "Integer")],
          responses=[resp("TraceJson", "Trace JSON", "List of {index, time, command, reply}", "String")]),
  prop("InstrumentInfo", "Instrument Info", "Model, driver and simulator description of the twin", "String"),
  prop("Status", "Status", "idle, busy or error, with the current operation", "String", observable=True),
  error("NotInitialized", "Not Initialized", "Call Initialize before liquid handling."),
  error("LiquidHandlingError", "Liquid Handling Error", "The twin refused or failed the operation (for example too little liquid, no tips, unknown resource); the message says why."),
])

HHS = feature("heatingshaking", "HeaterShakerService", "Heater Shaker Service",
  "A heater-shaker digital twin (first-order thermal model, accelerated time) that holds the reaction plate at 37 C and shakes it.", [
  command("SetTemperature", "Set Temperature", "Set the target temperature and wait until it is reached (within 0.5 C). Observable: reports the current temperature.",
          params=[param("TargetTemperature", "Target Temperature", "Target in degrees Celsius (4-70)", "Real")],
          responses=[resp("ReachedTemperature", "Reached Temperature", "Temperature when the target was reached, C", "Real")],
          intermediate=[inter("CurrentTemperature", "Current Temperature", "Current block temperature, C", "Real")], observable=True, errors=["TemperatureOutOfRange"]),
  command("StartShaking", "Start Shaking", "Start orbital shaking at a speed.",
          params=[param("Speed", "Speed", "Speed in rpm (200-3000)", "Integer")], responses=[MSG], errors=["SpeedOutOfRange"]),
  command("StopShaking", "Stop Shaking", "Stop shaking.", responses=[MSG]),
  prop("CurrentTemperature", "Current Temperature", "Current block temperature, C", "Real", observable=True),
  prop("ShakingSpeed", "Shaking Speed", "Current shaking speed in rpm (0 = stopped)", "Integer"),
  error("TemperatureOutOfRange", "Temperature Out Of Range", "Target must be between 4 and 70 C."),
  error("SpeedOutOfRange", "Speed Out Of Range", "Speed must be between 200 and 3000 rpm."),
])

here = Path(__file__).parent
(here / "LiquidHandlerService-v1_0.sila.xml").write_text(LH)
(here / "HeaterShakerService-v1_0.sila.xml").write_text(HHS)
print("wrote", [p.name for p in here.glob("*.sila.xml")])
