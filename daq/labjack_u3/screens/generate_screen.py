"""Generate a simple Phoebus screen for labjack_u3 PVs."""
__version__ = 'v0.0.2 2026-08-27'

import argparse
from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget

DEFAULT_PREFIX = "$(DEV):"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=__version__,
    )
    parser.add_argument("-t", "--title", default="LabJack U3", help="Screen title")
    parser.add_argument(
        "prefix",
        nargs="?",
        default=DEFAULT_PREFIX,
        help=(
            "PV prefix used for all widget PV names. "
            "If not specified, the prefix is `$(DEV):`, it can be defined in screen macros."
        ),
    )
    return parser.parse_args()


def _add_items(widget, values: str) -> None:
    for item in values.split(", "):
        widget.item(item)


def main() -> None:
    pargs = _parse_args()
    prefix = pargs.prefix

    screen = phoebusgen.screen.Screen(pargs.title, "labjack_u3.bob")
    screen.width(1200)
    screen.height(840)

    w = phoebusgen.widget
    widgets = {
        "title": w.Label("title", "LabJack U3", 20, 10, 200, 30),
        "version": w.TextUpdate("VERSION", f"{prefix}VERSION", 230, 14, 210, 20),
        "dateTime": w.TextUpdate("dateTime", f"{prefix}dateTime", 450, 14, 210, 20),

        "state_lbl": w.Label("state_lbl", "Run/Stop:", 20, 45, 70, 20),
        "server": w.ComboBox("server", f"{prefix}server", 95, 45, 110, 20),
        "sleep_lbl": w.Label("sleep_lbl", "Sleep [s]:", 220, 45, 65, 20),
        "sleep": w.TextEntry("sleep", f"{prefix}sleep", 290, 45, 80, 20),
        "poll_lbl": w.Label("poll_lbl", "Poll Cnt:", 390, 45, 60, 20),
        "cycleTime": w.TextUpdate("cycleTime", f"{prefix}cycleTime", 455, 45, 95, 20),
        "cycle_lbl": w.Label("cycle_lbl", "Cycle:", 565, 45, 40, 20),
        "cycle": w.TextUpdate("cycle", f"{prefix}cycle", 610, 45, 95, 20),
        "rps_lbl": w.Label("rps_lbl", "RPS:", 720, 45, 30, 20),
        "rps": w.TextUpdate("rps", f"{prefix}rps", 755, 45, 75, 20),
        "temp_lbl": w.Label("temp_lbl", "Temp [C]:", 845, 45, 65, 20),
        "tempU3": w.TextUpdate("tempU3", f"{prefix}tempU3", 915, 45, 80, 20),
        "hardPoll_lbl": w.Label("hardPoll_lbl", "HW Poll [s]:", 1010, 45, 80, 20),
        "hardPoll": w.TextEntry("hardPoll", f"{prefix}hardPoll", 1095, 45, 80, 20),

        "analog_lbl": w.Label("analog_lbl", "Analog", 20, 85, 100, 20),
        "DAC0_lbl": w.Label("DAC0_lbl", "DAC0 [V]:", 20, 110, 70, 20),
        "DAC0": w.TextEntry("DAC0", f"{prefix}DAC0", 95, 110, 110, 20),
        "DAC1_lbl": w.Label("DAC1_lbl", "DAC1 [V]:", 220, 110, 70, 20),
        "DAC1": w.TextEntry("DAC1", f"{prefix}DAC1", 295, 110, 110, 20),
        "AIN_HV_lbl": w.Label("AIN_HV_lbl", "AIN_HV [V]:", 20, 138, 70, 20),
        "AIN_HV": w.TextUpdate("AIN_HV", f"{prefix}AIN_HV", 95, 138, 500, 20),
        "AIN_LV_lbl": w.Label("AIN_LV_lbl", "AIN_LV [V]:", 20, 166, 70, 20),
        "AIN_LV": w.TextUpdate("AIN_LV", f"{prefix}AIN_LV", 95, 166, 500, 20),
        "Count_lbl": w.Label("Count_lbl", "Count:", 620, 138, 45, 20),
        "Count": w.TextUpdate("Count", f"{prefix}Count", 670, 138, 260, 20),
        "cfg_lbl": w.Label("cfg_lbl", "configFIO:", 620, 166, 60, 20),
        "configFIO": w.TextUpdate("configFIO", f"{prefix}configFIO", 685, 166, 490, 20),

        "dio_lbl": w.Label("dio_lbl", "DIO states", 20, 210, 100, 20),
    }

    x0 = 20
    y0 = 235
    dx = 145
    dy = 28
    for io_num in range(12,16):
        col = io_num % 8
        row = io_num // 8
        x = x0 + col * dx
        y = y0 + row * dy
        widgets[f"DIO{io_num}_lbl"] = w.Label(f"DIO{io_num}_lbl", f"DIO{io_num}:", x, y, 45, 20)
        widgets[f"DIO{io_num}"] = w.ComboBox(f"DIO{io_num}", f"{prefix}DIO{io_num}", x + 50, y, 80, 20)

    widgets["pulse_lbl"] = w.Label("pulse_lbl", "Pulse", 20, 302, 100, 20)
    widgets["pulseTick_lbl"] = w.Label("pulseTick_lbl", "tick [s]:", 20, 327, 55, 20)
    widgets["pulseTick"] = w.TextUpdate("pulseTick", f"{prefix}pulseTick", 80, 327, 90, 20)
    widgets["Pulse_lbl"] = w.Label("Pulse_lbl", "Select pulse:", 190, 327, 70, 20)
    widgets["Pulse"] = w.ComboBox("Pulse", f"{prefix}Pulse", 265, 327, 160, 20)

    y_pars0 = 355
    for i in range(4,8):
        y = y_pars0 + i * 25
        if i == 5:
            widgets[f"PulseFIO{i}_lbl"] = w.Label(f"PulseFIO{i}_lbl", f"PulseFIO{i}Pars:", 20, y, 95, 20)
            widgets[f"PulseFIO{i}Pars"] = w.TextEntry(f"PulseFIO{i}Pars", f"{prefix}PulseFIO{i}Pars", 120, y, 300, 20)
        widgets[f"PulseEIO{i}_lbl"] = w.Label(f"PulseEIO{i}_lbl", f"PulseEIO{i}Pars:", 450, y, 95, 20)
        widgets[f"PulseEIO{i}Pars"] = w.TextEntry(f"PulseEIO{i}Pars", f"{prefix}PulseEIO{i}Pars", 550, y, 300, 20)

    widgets["pwm_lbl"] = w.Label("pwm_lbl", "PWM", 890, 302, 80, 20)
    widgets["PWM_period_lbl"] = w.Label("PWM_period_lbl", "Period [ms]:", 890, 327, 75, 20)
    widgets["PWM_period"] = w.TextUpdate("PWM_period", f"{prefix}PWM_period", 970, 327, 110, 20)
    widgets["PWM_multiplier_lbl"] = w.Label("PWM_multiplier_lbl", "Multiplier:", 890, 355, 75, 20)
    widgets["PWM_multiplier"] = w.TextEntry("PWM_multiplier", f"{prefix}PWM_multiplier", 970, 355, 110, 20)
    widgets["PWM_pulseWidth_lbl"] = w.Label("PWM_pulseWidth_lbl", "Pulse [ms]:", 890, 383, 75, 20)
    widgets["PWM_pulseWidth"] = w.TextEntry("PWM_pulseWidth", f"{prefix}PWM_pulseWidth", 970, 383, 110, 20)

    _add_items(widgets["server"], "Start, Stop, Clear, Exit, Started, Stopped, Exited")
    for io_num in range(12,16):
        _add_items(widgets[f"DIO{io_num}"], "0, 1")

    pulse_items = ["PulseFIO5"] + [f"PulseEIO{i}" for i in range(8)]
    for item in pulse_items:
        widgets["Pulse"].item(item)

    widgets["sleep"].precision(2)
    widgets["hardPoll"].precision(2)
    widgets["DAC0"].format("Engineering")
    widgets["DAC0"].precision(3)
    widgets["DAC1"].format("Engineering")
    widgets["DAC1"].precision(3)
    #widgets["pollCount"].format("Decimal")
    #widgets["pollCount"].precision(0)
    widgets["cycle"].format("Decimal")
    widgets["cycle"].precision(0)
    widgets["rps"].format("Engineering")
    widgets["rps"].precision(2)
    widgets["tempU3"].format("Engineering")
    widgets["tempU3"].precision(2)
    widgets["pulseTick"].format("Engineering")
    widgets["pulseTick"].precision(6)
    widgets["PWM_period"].format("Engineering")
    widgets["PWM_period"].precision(3)
    widgets["PWM_multiplier"].format("Decimal")
    widgets["PWM_multiplier"].precision(0)
    widgets["PWM_pulseWidth"].format("Engineering")
    widgets["PWM_pulseWidth"].precision(3)

    screen.add_widget(list(widgets.values()))

    out = Path(__file__).with_name("labjack_u3.bob")
    screen.write_screen(str(out))


if __name__ == "__main__":
    main()
