"""Generate a simple Phoebus screen for Siglent SDG PVs."""
__version__ = 'v0.0.2 2026-08-26'

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
	parser.add_argument("-t", "--title", default="Siglent SDG", help="Screen title")
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


def main() -> None:
	pargs = _parse_args()
	prefix = pargs.prefix

	screen = phoebusgen.screen.Screen(pargs.title, "siglent_sdg.bob")
	screen.width(980)
	screen.height(420)

	w = phoebusgen.widget
	widgets = {
		"title": w.Label("title", "Siglent SDG", 20, 10, 180, 30),
		"genIDN": w.TextUpdate("genIDN", f"{prefix}genIDN", 210, 10, 520, 20),
		"dateTime": w.TextUpdate("dateTime", f"{prefix}dateTime", 740, 10, 210, 20),

		"state_lbl": w.Label("state_lbl", "Run/Stop:", 20, 42, 70, 20),
		"server": w.ComboBox("server", f"{prefix}server", 95, 42, 110, 20),
		"sleep_lbl": w.Label("sleep_lbl", "Sleep [s]:", 220, 42, 65, 20),
		"sleep": w.TextEntry("sleep", f"{prefix}sleep", 290, 42, 80, 20),
		"poll_lbl": w.Label("poll_lbl", "Poll Count:", 390, 42, 70, 20),
		"pollCount": w.TextUpdate("pollCount", f"{prefix}pollCount", 470, 42, 110, 20),

		"ch1_lbl": w.Label("ch1_lbl", "Channel 1", 20, 80, 90, 20),
		"c01Output_lbl": w.Label("c01Output_lbl", "Output:", 20, 105, 55, 20),
		"c01Output": w.ComboBox("c01Output", f"{prefix}c01Output", 80, 105, 80, 20),
		"c01Load_lbl": w.Label("c01Load_lbl", "Load:", 175, 105, 40, 20),
		"c01Load": w.ComboBox("c01Load", f"{prefix}c01Load", 220, 105, 70, 20),
		"c01Polarity_lbl": w.Label("c01Polarity_lbl", "Polarity:", 305, 105, 55, 20),
		"c01Polarity": w.ComboBox("c01Polarity", f"{prefix}c01Polarity", 365, 105, 80, 20),
		"c01WaveType_lbl": w.Label("c01WaveType_lbl", "Wave:", 460, 105, 45, 20),
		"c01WaveType": w.ComboBox("c01WaveType", f"{prefix}c01WaveType", 510, 105, 95, 20),
		"c01Frequency_lbl": w.Label("c01Frequency_lbl", "Freq [Hz]:", 620, 105, 60, 20),
		"c01Frequency": w.TextEntry("c01Frequency", f"{prefix}c01Frequency", 685, 105, 110, 20),
		"c01Amplitude_lbl": w.Label("c01Amplitude_lbl", "Amp [Vpp]:", 810, 105, 65, 20),
		"c01Amplitude": w.TextEntry("c01Amplitude", f"{prefix}c01Amplitude", 880, 105, 80, 20),
		"c01Offset_lbl": w.Label("c01Offset_lbl", "Offset [V]:", 620, 130, 60, 20),
		"c01Offset": w.TextEntry("c01Offset", f"{prefix}c01Offset", 685, 130, 110, 20),
		"c01Phase_lbl": w.Label("c01Phase_lbl", "Phase [deg]:", 810, 130, 65, 20),
		"c01Phase": w.TextEntry("c01Phase", f"{prefix}c01Phase", 880, 130, 80, 20),

		"ch2_lbl": w.Label("ch2_lbl", "Channel 2", 20, 185, 90, 20),
		"c02Output_lbl": w.Label("c02Output_lbl", "Output:", 20, 210, 55, 20),
		"c02Output": w.ComboBox("c02Output", f"{prefix}c02Output", 80, 210, 80, 20),
		"c02Load_lbl": w.Label("c02Load_lbl", "Load:", 175, 210, 40, 20),
		"c02Load": w.ComboBox("c02Load", f"{prefix}c02Load", 220, 210, 70, 20),
		"c02Polarity_lbl": w.Label("c02Polarity_lbl", "Polarity:", 305, 210, 55, 20),
		"c02Polarity": w.ComboBox("c02Polarity", f"{prefix}c02Polarity", 365, 210, 80, 20),
		"c02WaveType_lbl": w.Label("c02WaveType_lbl", "Wave:", 460, 210, 45, 20),
		"c02WaveType": w.ComboBox("c02WaveType", f"{prefix}c02WaveType", 510, 210, 95, 20),
		"c02Frequency_lbl": w.Label("c02Frequency_lbl", "Freq [Hz]:", 620, 210, 60, 20),
		"c02Frequency": w.TextEntry("c02Frequency", f"{prefix}c02Frequency", 685, 210, 110, 20),
		"c02Amplitude_lbl": w.Label("c02Amplitude_lbl", "Amp [Vpp]:", 810, 210, 65, 20),
		"c02Amplitude": w.TextEntry("c02Amplitude", f"{prefix}c02Amplitude", 880, 210, 80, 20),
		"c02Offset_lbl": w.Label("c02Offset_lbl", "Offset [V]:", 620, 235, 60, 20),
		"c02Offset": w.TextEntry("c02Offset", f"{prefix}c02Offset", 685, 235, 110, 20),
		"c02Phase_lbl": w.Label("c02Phase_lbl", "Phase [deg]:", 810, 235, 65, 20),
		"c02Phase": w.TextEntry("c02Phase", f"{prefix}c02Phase", 880, 235, 80, 20),

		"scpi_lbl": w.Label("scpi_lbl", "SCPI:", 20, 320, 40, 20),
		"instrCmdS": w.TextEntry("instrCmdS", f"{prefix}instrCmdS", 65, 320, 250, 20),
		"reply_lbl": w.Label("reply_lbl", "Reply:", 330, 320, 40, 20),
		"instrCmdR": w.TextUpdate("instrCmdR", f"{prefix}instrCmdR", 375, 320, 585, 20),
		"instrCmd2S": w.TextEntry("instrCmd2S", f"{prefix}instrCmd2S", 65, 340, 250, 20),
	}

	for item in "Start, Stop, Clear, Exit, Started, Stopped, Exited".split(", "):
		widgets["server"].item(item)

	for ch in ("c01", "c02"):
		for item in "OFF, ON".split(", "):
			widgets[f"{ch}Output"].item(item)
		for item in "50, HZ".split(", "):
			widgets[f"{ch}Load"].item(item)
		for item in "NOR, INVT".split(", "):
			widgets[f"{ch}Polarity"].item(item)
		for item in "SINE, SQUARE, RAMP, PULSE, NOISE, ARB, DC, PRBS".split(", "):
			widgets[f"{ch}WaveType"].item(item)

	widgets["sleep"].precision(2)
	widgets["pollCount"].format("Decimal")
	widgets["pollCount"].precision(0)

	for name in ("c01Frequency", "c02Frequency"):
		widgets[name].format("Exponential")
		widgets[name].precision(3)
	for name in ("c01Amplitude", "c02Amplitude", "c01Offset", "c02Offset", "c01Phase", "c02Phase"):
		widgets[name].format("Engineering")
		widgets[name].precision(3)

	widgets["instrCmdR"].wrap_words(False)

	screen.add_widget(list(widgets.values()))

	out = Path(__file__).with_name("siglent_sdg.bob")
	screen.write_screen(str(out))


if __name__ == "__main__":
	main()
