"""Generate a simple Phoebus screen for Keysight DSO-X PVs."""

from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget


def main() -> None:
    screen = phoebusgen.screen.Screen("simplescope", "simplescope.bob")
    screen.width(980)
    screen.height(360)

    widgets = [
        phoebusgen.widget.Label("title", "SimpleScope", 20, 10, 220, 30),
        phoebusgen.widget.Label("idn_lbl", "Scope ID", 20, 52, 140, 24),
        phoebusgen.widget.TextUpdate("idn", "KDSOX:scopeIDN", 170, 50, 780, 26),

        phoebusgen.widget.Label("state_lbl", "Trigger State", 20, 88, 140, 24),
        phoebusgen.widget.TextUpdate("state", "KDSOX:trigState", 170, 86, 180, 26),

        phoebusgen.widget.Label("acq_lbl", "Acq Count", 380, 88, 120, 24),
        phoebusgen.widget.TextUpdate("acq", "KDSOX:acqCount", 500, 86, 110, 26),

        phoebusgen.widget.Label("lost_lbl", "Lost Trigs", 640, 88, 120, 24),
        phoebusgen.widget.TextUpdate("lost", "KDSOX:lostTrigs", 760, 86, 110, 26),

        phoebusgen.widget.Label("run_lbl", "Run/Stop", 20, 124, 140, 24),
        phoebusgen.widget.ComboBox("run", "KDSOX:instrCtrl", 170, 122, 180, 26),

        phoebusgen.widget.Label("time_lbl", "Time/Div [s/div]", 380, 124, 160, 24),
        phoebusgen.widget.TextEntry("time", "KDSOX:timePerDiv", 540, 122, 120, 26),

        phoebusgen.widget.Label("trig_lvl_lbl", "Trig Level [V]", 680, 124, 120, 24),
        phoebusgen.widget.TextEntry("trig_lvl", "KDSOX:trigLevel", 800, 122, 120, 26),

        phoebusgen.widget.Label("wf_lbl", "CH1 Waveform", 20, 164, 140, 24),
        phoebusgen.widget.XYPlot("wf_plot", 20, 190, 930, 150),
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
    y_axis = phoebusgen.widget.XYPlotYAxis()
    y_axis.title("Volts")
    trace = phoebusgen.widget.XYPlotTrace()
    trace.name("CH1")
    trace.y_pv("KDSOX:c01Waveform")
    plot.add_x_axis(x_axis)
    plot.add_y_axis(y_axis)
    plot.add_trace(trace)

    screen.add_widget(widgets)

    out = Path(__file__).with_name("simplescope.bob")
    screen.write_screen(str(out))


if __name__ == "__main__":
    main()
