"""Operator interface generator for template"""
__version__ = 'v0.0.1 2026-10-01'
# pylint: disable=invalid-name,broad-exception-caught

import argparse
from pathlib import Path

import phoebusgen.screen
import phoebusgen.widget

DEVICE = "template"
INSTANCE = "0"
TITLE = DEVICE+INSTANCE
PREFIX = f'pva://{DEVICE}:{INSTANCE}:'

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=__version__,
    )
    parser.add_argument("-t", "--title", default=TITLE, help="Screen title")
    parser.add_argument("prefix", nargs="?", default=PREFIX,
        help=(
            "PV prefix used for all widget PV names. "
        ),
    )
    return parser.parse_args()

def _add_items(widget, values: str) -> None:
    for item in values.split(", "):
        widget.item(item)

def main() -> None:
    pargs = _parse_args()
    prefix = pargs.prefix

    screen = phoebusgen.screen.Screen(pargs.title, f"{TITLE}.bob")
    screen.width(1080)
    screen.height(660)

    w = phoebusgen.widget
    widgets = {
        "title": w.Label("title", TITLE, 20, 10, 170, 30),
        "Model_lbl": w.Label("Model_lbl", "Model:", 200, 14, 40, 20),
        "Model": w.TextUpdate("Model", f"{prefix}Model", 245, 14, 80, 20),
        "Version_lbl": w.Label("Version_lbl", "FW:", 340, 14, 25, 20),
        "Version": w.TextUpdate("Version", f"{prefix}Version", 365, 14, 40, 20),
        "dateTime": w.TextUpdate("dateTime", f"{prefix}dateTime", 420, 14, 70, 20),
    }
    y = 45
    widgets.update({
        "srvStatus_lbl": w.Label("srvStatus_lbl", "Server:", 20, y, 100, 20),
        "srvStatus": w.TextUpdate("srvStatus", f"{prefix}status", 70, y, 790, 20),
    })
    y += 40
    widgets.update({
        "state_lbl": w.Label("state_lbl", "Run/Stop:", 20, y, 65, 20),
        "server": w.ComboBox("server", f"{prefix}server", 90, y, 110, 20),
        "sleep_lbl": w.Label("sleep_lbl", "Sleep:", 410, y, 40, 20),
        "sleep": w.TextEntry("sleep", f"{prefix}sleep", 450, y, 50, 20),
        "cycle_lbl": w.Label("cycle_lbl", "Cycle:", 520, y, 40, 20),
        "cycleTime": w.TextUpdate("cycleTime", f"{prefix}cycleTime", 560, y, 60, 20),
        "hb_lbl": w.Label("hb_lbl", "HB:", 640, y, 30, 20),
        "HEARTBEAT": w.TextUpdate("HEARTBEAT", f"{prefix}HEARTBEAT", 670, y, 70, 20),
    })

    # TODO: add device widgets

    screen.add_widget(list(widgets.values()))

    out = Path(__file__).with_name(f"{TITLE}.bob")
    screen.write_screen(str(out))

if __name__ == "__main__":
    main()
