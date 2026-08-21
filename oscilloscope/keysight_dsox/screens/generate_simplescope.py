"""Generate a simple Phoebus screen for Keysight DSO-X PVs."""
__version__ = 'v0.0.1 2026-08-20'

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

    widgets = [
        phoebusgen.widget.Label("title", "SimpleScope", 20, 10, 220, 30),
        phoebusgen.widget.TextUpdate("idn", f"{prefix}scopeIDN", 120, 10, 270, 20),
        phoebusgen.widget.TextUpdate("vers", f"{prefix}VERSION", 410, 10, 140, 20),

        phoebusgen.widget.Label("state_lbl", "Trig State:", 20, 38, 70, 20),
        phoebusgen.widget.TextUpdate("state", f"{prefix}trigState", 120, 38, 40, 20),

        phoebusgen.widget.Label("acq_lbl", "Acq Count:", 380, 38, 80, 20),
        phoebusgen.widget.TextUpdate("acqCount", f"{prefix}acqCount", 460, 38, 60, 20),

        phoebusgen.widget.Label("lost_lbl", "Lost Trigs:", 540, 38, 70, 20),
        phoebusgen.widget.TextUpdate("lostTrigs", f"{prefix}lostTrigs", 620, 38, 60, 20),

        phoebusgen.widget.Label("run_lbl", "Run/Stop:", 20, 60, 70, 20),
        phoebusgen.widget.ComboBox("run", f"{prefix}instrCtrl", 120, 60, 60, 20),

        phoebusgen.widget.Label("time_lbl", "Time/Div:", 200, 60, 70, 20),
        phoebusgen.widget.TextEntry("time", f"{prefix}timePerDiv", 270, 60, 110, 20),

        phoebusgen.widget.Label("reclen_lbl", "RecLength:", 400, 60, 80, 20),
        phoebusgen.widget.TextEntry("reclenS", f"{prefix}recLengthS", 480, 60, 80, 20),
        phoebusgen.widget.TextEntry("reclenR", f"{prefix}recLengthR", 560, 60, 80, 20),
        phoebusgen.widget.Label("samplingRate_lbl", "SRate:", 650, 60, 60, 20),
        phoebusgen.widget.TextUpdate("samplingRate", f"{prefix}samplingRate", 700, 60, 80, 20),

        phoebusgen.widget.Label("trigSource_lbl", "Source:", 20, 90, 90, 20),
        phoebusgen.widget.ComboBox("trigSource", f"{prefix}trigSource", 110, 90, 90, 20),  
        phoebusgen.widget.Label("trig_lvl_lbl", "Level:", 230, 90, 40, 20),
        phoebusgen.widget.TextEntry("trig_lvl", f"{prefix}trigLevel", 280, 90, 70, 20),
        phoebusgen.widget.Label("trigSlope_lbl", "Slope:", 360, 90, 60, 20),
        phoebusgen.widget.ComboBox("trigSlope", f"{prefix}trigSlope", 420, 90, 70, 20),
        phoebusgen.widget.Label("trigMode_lbl", "Mode:", 500, 90, 60, 20),
        phoebusgen.widget.ComboBox("trigMode", f"{prefix}trigMode", 560, 90, 80, 20),

        phoebusgen.widget.Label("wf_lbl", "Waveforms", 10, 110, 960, 420),
        phoebusgen.widget.XYPlot("wf_plot", 10, 130, 930, 430),

        phoebusgen.widget.Label("onoff_lbl", "On/Off:", 10, 560, 70, 20),
        phoebusgen.widget.BooleanButton("onoff1", f"{prefix}c01OnOff", 90, 560, 100, 20),
        phoebusgen.widget.BooleanButton("onoff2", f"{prefix}c02OnOff", 210, 560, 100, 20),
        phoebusgen.widget.BooleanButton("onoff3", f"{prefix}c03OnOff", 330, 560, 100, 20),
        phoebusgen.widget.BooleanButton("onoff4", f"{prefix}c04OnOff", 450, 560, 100, 20),

        phoebusgen.widget.Label("vpd_lbl", "Volts/Div:", 10, 585, 70, 20),
        phoebusgen.widget.TextEntry("vpd1", f"{prefix}c01VoltsPerDiv", 90, 585, 100, 20),
        phoebusgen.widget.TextEntry("vpd2", f"{prefix}c02VoltsPerDiv", 210, 585, 100, 20),
        phoebusgen.widget.TextEntry("vpd3", f"{prefix}c03VoltsPerDiv", 330, 585, 100, 20),
        phoebusgen.widget.TextEntry("vpd4", f"{prefix}c04VoltsPerDiv", 450, 585, 100, 20),

        phoebusgen.widget.Label("voff_lbl", "Volt Offset:", 10, 610, 70, 20),
        phoebusgen.widget.TextEntry("voff1", f"{prefix}c01VoltOffset", 90, 610, 100, 20),
        phoebusgen.widget.TextEntry("voff2", f"{prefix}c02VoltOffset", 210, 610, 100, 20),
        phoebusgen.widget.TextEntry("voff3", f"{prefix}c03VoltOffset", 330, 610, 100, 20),
        phoebusgen.widget.TextEntry("voff4", f"{prefix}c04VoltOffset", 450, 610, 100, 20),

        phoebusgen.widget.Label("scpi_lbl", "SCPI:", 10, 640, 50, 20),
        phoebusgen.widget.TextEntry("scpiS", f"{prefix}instrCmdS", 50, 640, 200, 20),
        phoebusgen.widget.TextEntry("scpiR", f"{prefix}instrCmdR", 260, 640, 550, 20),
    ]
    # Configure the run abd time widgets with appropriate items and formats
    for w in widgets:
        wname = w.get_element_value("name") 
        if wname == "run":
            w.item("Run")
            w.item("Stop")
            w.item("AutoScale")
            #w.item("*CLS")
        elif wname == "trigSlope":
            w.item("POS")
            w.item("NEG")
            w.item("EITH")
        elif wname == "trigMode":
            w.item("NORM")
            w.item("AUTO")
        elif wname == "time":
            w.format('Engineering')
        elif wname == "samplingRate":
            w.format('Exponential')
        #elif wname in ["vpd1", "vpd2", "vpd3", "vpd4", "voff1", "voff2", "voff3", "voff4"]:
        #    w.format('Engineering')
        elif wname in ["acqCount", "lostTrigs"]:
            w.format('Decimal')
            w.precision(0)
        elif wname in ["trigLevel"]:
            w.format('Engineering')
            w.precision(3)
        elif wname == 'tigSource':
            w.item("CHAN1")
            w.item("CHAN2")
            w.item("CHAN3")
            w.item("CHAN4")
            w.item("EXT")
            w.item("LINE")

    # Configure waveform traces using tAxis as x and channel waveform as y.
    plot = next(w for w in widgets if w.get_element_value("name") == "wf_plot")
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

    screen.add_widget(widgets)

    out = Path(__file__).with_name("simplescope.bob")
    screen.write_screen(str(out))

if __name__ == "__main__":
    main()
