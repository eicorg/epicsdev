"""Generate a simple Phoebus screen for labjack_u3 PVs."""
__version__ = 'v0.0.2 2026-08-27'

import argparse
from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget

DEFAULT_PREFIX = "$(DEV):"
DIOS = [5,12,13,14,15]# Digital/pulsed I/O numbers, 0-7 are FIO, 8-15 are EIO

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
        "poll_lbl": w.Label("poll_lbl", "Period:", 390, 45, 60, 20),
        "cycleTime": w.TextUpdate("cycleTime", f"{prefix}cycleTime", 450, 45, 60, 20),
        "cycle_lbl": w.Label("cycle_lbl", "Cycle:", 520, 45, 40, 20),
        "cycle": w.TextUpdate("cycle", f"{prefix}cycle", 560, 45, 60, 20),
        "temp_lbl": w.Label("temp_lbl", "Tempr:", 620, 45, 50, 20),
        "tempU3": w.TextUpdate("tempU3", f"{prefix}tempU3", 670, 45, 50, 20),

        "analog_lbl": w.Label("analog_lbl", "Analog IOs", 20, 85, 100, 20),
        "cfg_lbl": w.Label("cfg_lbl", "Config:", 130, 85, 70, 20),
        "configFIO": w.TextUpdate("configFIO", f"{prefix}configFIO", 210, 85, 250, 20),
        "DAC0_lbl": w.Label("DAC0_lbl", "DAC0 [V]:", 20, 110, 70, 20),
        "DAC0": w.TextEntry("DAC0", f"{prefix}DAC0", 95, 110, 110, 20),
        "DAC1_lbl": w.Label("DAC1_lbl", "DAC1 [V]:", 220, 110, 70, 20),
        "DAC1": w.TextEntry("DAC1", f"{prefix}DAC1", 295, 110, 110, 20),
        "AIN_HV_lbl": w.Label("AIN_HV_lbl", "AIN_HV [V]:", 20, 138, 70, 20),
        "AIN_HV": w.TextUpdate("AIN_HV", f"{prefix}AIN_HV", 95, 138, 300, 20),
        "AIN_LV_lbl": w.Label("AIN_LV_lbl", "AIN_LV [V]:", 20, 166, 70, 20),
        "AIN_LV": w.TextUpdate("AIN_LV", f"{prefix}AIN_LV", 95, 166, 300, 20),
        "Count_lbl": w.Label("Count_lbl", "Count:", 400, 138, 45, 20),
        "Count": w.TextUpdate("Count", f"{prefix}Count", 450, 138, 80, 20),
        "frequency": w.TextUpdate("frequency", f"{prefix}frequency", 540, 138, 80, 20),

        "dio_lbl": w.Label("dio_lbl", "Digital IOs", 20, 210, 100, 20),
    }
    x0 = 20
    y0 = 235
    dx = 100
    dy = 25
    for i, io_num in enumerate(DIOS):
        col = i % 8
        row = i // 8
        x = x0 + col * dx
        y = y0 + row * dy
        widgets[f"DIO{io_num}_lbl"] = w.Label(f"DIO{io_num}_lbl", f"DIO{io_num}:", x, y, 45, 20)
        widg = w.BooleanButton(f"DIO{io_num}", f"{prefix}DIO{io_num}", x + 50, y, 40, 20)
        #widg.format('Decimal')
        #widg.precision(0)
        widgets[f"DIO{io_num}"] = widg

    y += dy
    widgets["pulse_lbl"] = w.Label("pulse_lbl", "Pulsing Control", 20, y, 100, 20)
    y += dy
    widgets["pulseTick_lbl"] = w.Label("pulseTick_lbl", "tick [s]:", 20, y, 55, 20)    
    widgets["pulseTick"] = w.TextUpdate("pulseTick", f"{prefix}pulseTick", 80, y, 90, 20)
    widgets["pulseTick"].format("Engineering")
    widgets["pulseTick"].precision(3)
    widgets["Pulse_lbl"] = w.Label("Pulse_lbl", "Select&pulse:", 190, y, 90, 20)
    widgets["Pulse"] = w.ComboBox("Pulse", f"{prefix}Pulse", 280, y, 100, 20)

    yPulse = y
    for n,i in enumerate(DIOS):
        y += dy
        widgets[f"PulseIO{i}_lbl"] = w.Label(f"PulseIO{i}_lbl", f"PulseIO{i}Pars:", 20, y, 95, 20)
        widg = w.TextEntry(f"PulseIO{i}Pars", f"{prefix}PulseIO{i}Pars", 120, y, 300, 20)
        widg.format('Decimal')
        widg.precision(0)
        widgets[f"PulseIO{i}Pars"] = widg

    y = yPulse
    widgets["pwm_lbl"] = w.Label("pwm_lbl", "PWM", 450, y, 80, 20)
    y += dy
    widgets["PWM_period_lbl"] = w.Label("PWM_period_lbl", "Period [ms]:", 450, y, 75, 20)
    widgets["PWM_period"] = w.TextUpdate("PWM_period", f"{prefix}PWM_period", 530, y, 110, 20)
    y += dy
    widgets["PWM_multiplier_lbl"] = w.Label("PWM_multiplier_lbl", "Multiplier:", 450, y, 75, 20)
    widgets["PWM_multiplier"] = w.TextEntry("PWM_multiplier", f"{prefix}PWM_multiplier", 530, y, 110, 20)
    y += dy
    widgets["PWM_pulseWidth_lbl"] = w.Label("PWM_pulseWidth_lbl", "Pulse [ms]:", 450, y, 75, 20)
    widgets["PWM_pulseWidth"] = w.TextEntry("PWM_pulseWidth", f"{prefix}PWM_pulseWidth", 530, y, 110, 20)

    _add_items(widgets["server"], "Start, Stop, Clear, Exit, Started, Stopped, Exited")
    #for io_num in range(12,16):
    #    _add_items(widgets[f"DIO{io_num}"], "0, 1")

    pulse_items = [f"PulseIO{i}" for i in DIOS]
    for item in pulse_items:
        widgets["Pulse"].item(item)

    widgets["sleep"].precision(3)
    #widgets["cycleTime"].format("Engineering")
    widgets["cycleTime"].precision(4)
    widgets["DAC0"].format("Engineering")
    widgets["DAC0"].precision(3)
    widgets["DAC1"].format("Engineering")
    widgets["DAC1"].precision(3)
    widgets["cycle"].format("Decimal")
    widgets["cycle"].precision(0)
    widgets["tempU3"].format("Decimal")
    widgets["tempU3"].precision(1)
    widgets["PWM_period"].format("Engineering")
    widgets["PWM_period"].precision(3)
    widgets["PWM_multiplier"].format("Decimal")
    widgets["PWM_multiplier"].precision(0)
    widgets["PWM_pulseWidth"].format("Decimal")
    widgets["PWM_pulseWidth"].precision(3)
    widgets["Count"].format("Decimal")
    widgets["Count"].precision(0)

    screen.add_widget(list(widgets.values()))

    out = Path(__file__).with_name("labjack_u3.bob")
    screen.write_screen(str(out))


if __name__ == "__main__":
    main()
