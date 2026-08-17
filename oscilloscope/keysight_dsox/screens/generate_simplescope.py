"""Generate a simple Phoebus screen for Keysight DSO-X PVs."""

from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget

PREFIX = "$(DEV):"

def main() -> None:
    screen = phoebusgen.screen.Screen("simplescope", "simplescope.bob")
    screen.width(980)
    screen.height(360)

    widgets = [
        phoebusgen.widget.Label("title", "SimpleScope", 20, 10, 220, 30),
        phoebusgen.widget.TextUpdate("idn", "${PREFIX}scopeIDN", 120, 10, 270, 20),
        phoebusgen.widget.TextUpdate("vers", "${PREFIX}VERSION", 410, 10, 140, 20),

        phoebusgen.widget.Label("state_lbl", "Trig State:", 20, 38, 70, 20),
        phoebusgen.widget.TextUpdate("state", "${PREFIX}trigState", 170, 38, 70, 20),

        phoebusgen.widget.Label("acq_lbl", "Acq Count:", 380, 38, 80, 20),
        phoebusgen.widget.TextUpdate("acq", "${PREFIX}acqCount", 460, 38, 60, 20),

        phoebusgen.widget.Label("lost_lbl", "Lost Trigs:", 540, 38, 70, 20),
        phoebusgen.widget.TextUpdate("lost", "${PREFIX}lostTrigs", 620, 38, 60, 20),

        phoebusgen.widget.Label("run_lbl", "Run/Stop:", 20, 74, 70, 20),
        phoebusgen.widget.ComboBox("run", "${PREFIX}instrCtrl", 170, 74, 180, 20),

        phoebusgen.widget.Label("time_lbl", "Time/Div [s/div]", 220, 74, 70, 20),
        phoebusgen.widget.TextEntry("time", "${PREFIX}timePerDiv", 290, 74, 90, 20),

        phoebusgen.widget.Label("reclen_lbl", "RecLength:", 400, 74, 80, 20),
        phoebusgen.widget.TextEntry("reclenS", "${PREFIX}recLengthS", 480, 74, 80, 20),
        phoebusgen.widget.TextEntry("reclenR", "${PREFIX}recLengthR", 560, 74, 80, 20),

        phoebusgen.widget.Label("trig_lvl_lbl", "Trig Level:", 660, 74, 70, 20),
        phoebusgen.widget.TextEntry("trig_lvl", "${PREFIX}trigLevel", 730, 74, 70, 20),

        phoebusgen.widget.Label("wf_lbl", "Waveforms", 10, 110, 960, 420),
        phoebusgen.widget.XYPlot("wf_plot", 10, 130, 930, 430),

        phoebusgen.widget.Label("scpi_lbl", "SCPI:", 10, 580, 50, 20),
        phoebusgen.widget.TextEntry("scpiS", "${PREFIX}instrCmdS", 80, 580, 110, 20),
        phoebusgen.widget.TextEntry("scpiR", "${PREFIX}instrCmdR", 200, 580, 760, 20),
    ]
    # Configure combo box choices directly for convenience.
    for w in widgets:
        if w.get_element_value("name") == "run":
            w.item("Run")
            w.item("Stop")
            w.item("AutoScale")
            w.item("*CLS")
            break

    # Configure a basic CH1 waveform plot using array index as x and waveform as y.
    plot = next(w for w in widgets if w.get_element_value("name") == "wf_plot")
    x_axis = phoebusgen.widget.XYPlotXAxis()
    x_axis.title("Samples")
    x_axis.auto_scale(True)
    y_axis = phoebusgen.widget.XYPlotYAxis()
    y_axis.title("Volts")
    y_axis.auto_scale(True)
    trace = phoebusgen.widget.XYPlotTrace()
    trace.name("CH1")
    trace.y_pv("${PREFIX}c01Waveform")
    plot.add_x_axis(x_axis)
    plot.add_y_axis(y_axis)
    plot.add_trace(trace)

    screen.add_widget(widgets)

    out = Path(__file__).with_name("simplescope.bob")
    screen.write_screen(str(out))

if __name__ == "__main__":
    main()
