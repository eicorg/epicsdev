"""Generate a simple Phoebus screen for Keysight DSO-X PVs."""
__version__ = 'v0.0.2a 2026-08-21'# refactored

import argparse
from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget

DEFAULT_PREFIX = "$(DEV):"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=__version__)
                                    
    parser.add_argument("-p", "--prefix", default=DEFAULT_PREFIX, help=
"PV prefix used for all widget PV names. If not specified, the prefix is `$(DEV):`, it could be defined in screen macros.",
    )
    return parser.parse_args()

def main() -> None:
    pargs = _parse_args()
    prefix = pargs.prefix

    screen = phoebusgen.screen.Screen("simplescope", "simplescope.bob")
    screen.width(980)
    screen.height(360)

    widgets = {
        "SimpleScope": phoebusgen.widget.Label("title", "SimpleScope", 20, 10, 220, 30),
        "scopIDN":  phoebusgen.widget.TextUpdate("scopeIDN", f"{prefix}scopeIDN", 120, 10, 270, 20),
        "VERSION": phoebusgen.widget.TextUpdate("VERSION", f"{prefix}VERSION", 410, 10, 140, 20),
        "state_lbl": phoebusgen.widget.Label("state_lbl", "Trig State:", 20, 38, 70, 20),
        "trigState": phoebusgen.widget.TextUpdate("trigState", f"{prefix}trigState", 100, 38, 40, 20),
        "sleep_lbl": phoebusgen.widget.Label("sleep_lbl", "Sleep:", 150, 38, 40, 20),
        "sleep": phoebusgen.widget.TextEntry("sleep", f"{prefix}sleep", 190, 38, 60, 20),
        "acq_lbl": phoebusgen.widget.Label("acq_lbl", "Acq Count:", 380, 38, 80, 20),
        "acqCount": phoebusgen.widget.TextUpdate("acqCount", f"{prefix}acqCount", 460, 38, 60, 20),
        "lost_lbl": phoebusgen.widget.Label("lost_lbl", "Lost Trigs:", 540, 38, 70, 20),
        "lostTrigs": phoebusgen.widget.TextUpdate("lostTrigs", f"{prefix}lostTrigs", 620, 38, 60, 20),

        "run_lbl": phoebusgen.widget.Label("run_lbl", "Run/Stop:", 20, 60, 70, 20),
        "server": phoebusgen.widget.ComboBox("server", f"{prefix}server", 100, 60, 80, 20),
        "time_lbl": phoebusgen.widget.Label("time_lbl", "Time/Div:", 200, 60, 70, 20),
        "timePerDiv": phoebusgen.widget.TextEntry("timePerDiv", f"{prefix}timePerDiv", 270, 60, 110, 20),
        "reclen_lbl": phoebusgen.widget.Label("reclen_lbl", "RecLength:", 400, 60, 80, 20),
        "reclenR": phoebusgen.widget.TextEntry("reclenR", f"{prefix}recLengthR", 480, 60, 80, 20),
        "reclenS": phoebusgen.widget.TextEntry("reclenS", f"{prefix}recLengthS", 560, 60, 80, 20),
        "samplingRate_lbl": phoebusgen.widget.Label("samplingRate_lbl", "SRate:", 650, 60, 60, 20),
        "samplingRate": phoebusgen.widget.TextUpdate("samplingRate", f"{prefix}samplingRate", 700, 60, 80, 20),

        "trigSource_lbl": phoebusgen.widget.Label("trigSource_lbl", "Trigger:", 20, 90, 90, 20),
        "trigSource": phoebusgen.widget.ComboBox("trigSource", f"{prefix}trigSource", 100, 90, 90, 20),  
        "trig_lvl_lbl": phoebusgen.widget.Label("trig_lvl_lbl", "Level:", 230, 90, 40, 20),
        "trigLevel": phoebusgen.widget.TextEntry("trigLevel", f"{prefix}trigLevel", 280, 90, 70, 20),
        "trigSlope_lbl": phoebusgen.widget.Label("trigSlope_lbl", "Slope:", 360, 90, 60, 20),
        "trigSlope": phoebusgen.widget.ComboBox("trigSlope", f"{prefix}trigSlope", 420, 90, 70, 20),
        "trigMode_lbl": phoebusgen.widget.Label("trigMode_lbl", "Mode:", 500, 90, 60, 20),
        "trigMode": phoebusgen.widget.ComboBox("trigMode", f"{prefix}trigMode", 560, 90, 80, 20),

        "wf_lbl": phoebusgen.widget.Label("wf_lbl", "Waveforms", 10, 110, 960, 420),
        "wf_plot": phoebusgen.widget.XYPlot("wf_plot", 10, 130, 930, 430),

        "OnOff_lbl": phoebusgen.widget.Label("OnOff_lbl", "On/Off:", 10, 560, 70, 20),
        "c01OnOff": phoebusgen.widget.BooleanButton("c01OnOff", f"{prefix}c01OnOff", 90, 560, 100, 20),
        "c02OnOff": phoebusgen.widget.BooleanButton("c02OnOff", f"{prefix}c02OnOff", 210, 560, 100, 20),
        "c03OnOff": phoebusgen.widget.BooleanButton("c03OnOff", f"{prefix}c03OnOff", 330, 560, 100, 20),
        "c04OnOff": phoebusgen.widget.BooleanButton("c04OnOff", f"{prefix}c04OnOff", 450, 560, 100, 20),
        "mean_lbl": phoebusgen.widget.Label("mean_lbl", "Mean [V]:", 10, 585, 70, 20),
        "c01Mean": phoebusgen.widget.TextUpdate("c01Mean", f"{prefix}c01Mean", 90, 585, 100, 20),
        "c02Mean": phoebusgen.widget.TextUpdate("c02Mean", f"{prefix}c02Mean", 210, 585, 100, 20),
        "c03Mean": phoebusgen.widget.TextUpdate("c03Mean", f"{prefix}c03Mean", 330, 585, 100, 20),
        "c04Mean": phoebusgen.widget.TextUpdate("c04Mean", f"{prefix}c04Mean", 450, 585, 100, 20),

        "rms_lbl": phoebusgen.widget.Label("rms_lbl", "RMS [V]:", 10, 610, 70, 20),
        "c01RMS": phoebusgen.widget.TextUpdate("c01RMS", f"{prefix}c01RMS", 90, 610, 100, 20),
        "c02RMS": phoebusgen.widget.TextUpdate("c02RMS", f"{prefix}c02RMS", 210, 610, 100, 20),
        "c03RMS": phoebusgen.widget.TextUpdate("c03RMS", f"{prefix}c03RMS", 330, 610, 100, 20),
        "c04RMS": phoebusgen.widget.TextUpdate("c04RMS", f"{prefix}c04RMS", 450, 610, 100, 20),

        "p2p_lbl": phoebusgen.widget.Label("p2p_lbl", "P2P [V]:", 10, 635, 70, 20),
        "c01Peak2Peak": phoebusgen.widget.TextUpdate("c01Peak2Peak", f"{prefix}c01Peak2Peak", 90, 635, 100, 20),
        "c02Peak2Peak": phoebusgen.widget.TextUpdate("c02Peak2Peak", f"{prefix}c02Peak2Peak", 210, 635, 100, 20),
        "c03Peak2Peak": phoebusgen.widget.TextUpdate("c03Peak2Peak", f"{prefix}c03Peak2Peak", 330, 635, 100, 20),
        "c04Peak2Peak": phoebusgen.widget.TextUpdate("c04Peak2Peak", f"{prefix}c04Peak2Peak", 450, 635, 100, 20),

        "vpd_lbl": phoebusgen.widget.Label("vpd_lbl", "Volts/Div:", 10, 660, 70, 20),
        "c01VoltsPerDiv": phoebusgen.widget.TextEntry("c01VoltsPerDiv", f"{prefix}c01VoltsPerDiv", 90, 660, 100, 20),
        "c02VoltsPerDiv": phoebusgen.widget.TextEntry("c02VoltsPerDiv", f"{prefix}c02VoltsPerDiv", 210, 660, 100, 20),
        "c03VoltsPerDiv": phoebusgen.widget.TextEntry("c03VoltsPerDiv", f"{prefix}c03VoltsPerDiv", 330, 660, 100, 20),
        "c04VoltsPerDiv": phoebusgen.widget.TextEntry("c04VoltsPerDiv", f"{prefix}c04VoltsPerDiv", 450, 660, 100, 20),

        "voff_lbl": phoebusgen.widget.Label("voff_lbl", "Volt Offset:", 10, 685, 70, 20),
        "c01VoltOffset": phoebusgen.widget.TextEntry("c01VoltOffset", f"{prefix}c01VoltOffset", 90, 685, 100, 20),
        "c02VoltOffset": phoebusgen.widget.TextEntry("c02VoltOffset", f"{prefix}c02VoltOffset", 210, 685, 100, 20),
        "c03VoltOffset": phoebusgen.widget.TextEntry("c03VoltOffset", f"{prefix}c03VoltOffset", 330, 685, 100, 20),
        "c04VoltOffset": phoebusgen.widget.TextEntry("c04VoltOffset", f"{prefix}c04VoltOffset", 450, 685, 100, 20),
        "scpi_lbl": phoebusgen.widget.Label("scpi_lbl", "SCPI:", 10, 715, 50, 20),
        "instrCmdS": phoebusgen.widget.TextEntry("instrCmdS", f"{prefix}instrCmdS", 50, 715, 200, 20),
        "instrCmdR": phoebusgen.widget.TextEntry("instrCmdR", f"{prefix}instrCmdR", 260, 715, 550, 20),
    }
    # Configure the server abd time widgets with appropriate items and formats
    for item in "Start, Stop, Clear, Exit, Started, Stopped, Exited".split(", "):
        widgets["server"].item(item)
    for item in "POS, NEG, EITH".split(", "):
        widgets["trigSlope"].item(item)
    for item in "NORM, AUTO".split(", "):
        widgets["trigMode"].item(item)
    widgets["sleep"].precision(1)
    widgets["timePerDiv"].format('Exponential')
    widgets["timePerDiv"].precision(1)
    widgets["reclenR"].format('Decimal')
    widgets["reclenR"].precision(0)
    widgets["samplingRate"].format('Exponential')
    widgets["samplingRate"].precision(1)
    widgets["acqCount"].format('Decimal')
    widgets["acqCount"].precision(0)
    widgets["lostTrigs"].format('Decimal')
    widgets["lostTrigs"].precision(0)
    widgets["trigLevel"].format('Engineering')
    widgets["trigLevel"].precision(3)
    for wname in ["c01Mean", "c02Mean", "c03Mean", "c04Mean", "c01RMS", "c02RMS", "c03RMS", "c04RMS", "c01Peak2Peak", "c02Peak2Peak", "c03Peak2Peak", "c04Peak2Peak"]:
        widgets[wname].format('Engineering')
        widgets[wname].precision(3)
    for item in "CHAN1, CHAN2, CHAN3, CHAN4, EXT, LINE".split(", "):
        widgets["trigSource"].item(item)

    # Configure waveform traces using tAxis as x and channel waveform as y.
    #plot = next(w for w in widgets if w.get_element_value("name") == "wf_plot")
    plot = widgets["wf_plot"]
    plot.show_toolbar(True)
    x_axis = phoebusgen.widget.XYPlotXAxis()
    x_axis.title("Time [s]")
    x_axis.auto_scale(True)
    x_axis.show_grid(True)
    y_axis = phoebusgen.widget.XYPlotYAxis()
    y_axis.title("Divisions")
    #y_axis.auto_scale(True)
    y_axis.minimum(0)
    y_axis.maximum(8)
    y_axis.show_grid(True)

    trace1 = phoebusgen.widget.XYPlotTrace()
    trace1.name("CH1")
    trace1.x_pv(f"{prefix}tAxis")
    trace1.y_pv(f"{prefix}c01Waveform")

    trace2 = phoebusgen.widget.XYPlotTrace()
    trace2.name("CH2")
    trace2.x_pv(f"{prefix}tAxis")
    trace2.y_pv(f"{prefix}c02Waveform")

    trace3 = phoebusgen.widget.XYPlotTrace()
    trace3.name("CH3")
    trace3.x_pv(f"{prefix}tAxis")
    trace3.y_pv(f"{prefix}c03Waveform")

    trace4 = phoebusgen.widget.XYPlotTrace()
    trace4.name("CH4")
    trace4.x_pv(f"{prefix}tAxis")
    trace4.y_pv(f"{prefix}c04Waveform")

    plot.add_x_axis(x_axis)
    plot.add_y_axis(y_axis)
    plot.add_trace(trace1)
    plot.add_trace(trace2)
    plot.add_trace(trace3)
    plot.add_trace(trace4)

    screen.add_widget(list(widgets.values()))

    out = Path(__file__).with_name("simplescope.bob")
    screen.write_screen(str(out))

if __name__ == "__main__":
    main()
