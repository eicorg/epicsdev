# siglent_sdg

EPICS PVAccess server for Siglent SDG signal generators, implemented with the `epicsdev` framework.

## Features

- EPICS PVAccess server lifecycle and diagnostics (`server`, `status`, `sleep`, `VERSION`, etc.)
- VISA connection to Siglent generators via SCPI
- Channel control PVs for:
	- Output ON/OFF
	- Load (50 Ω / high-Z)
	- Polarity
	- Waveform type
	- Frequency
	- Amplitude
	- Offset
	- Phase
- Raw SCPI passthrough PVs: `instrCmdS` and `instrCmdR`

## Default VISA Address

The default VISA resource is:

`TCPIP::192.168.50.90::INSTR`

Override it with `--resource`.

## Run

From this folder:

```bash
python -m siglent_sdg --device siglent --index 0
```

Common options:

- `-r, --resource` VISA resource string
- `-C, --channels` number of channels to expose (default: 2)
- `-d, --device` PV prefix device name
- `-i, --index` PV prefix index
- `-v, --verbose` increase log verbosity

Resulting PV prefix format:

`<device><index>:`

Example: `siglent0:`

## Main PVs

Global:

- `genIDN`, `dateTime`, `pollCount`
- `instrCmdS`, `instrCmdR`

Per channel (`c01`, `c02`, ...):

- `cNNOutput`
- `cNNLoad`
- `cNNPolarity`
- `cNNWaveType`
- `cNNFrequency`
- `cNNAmplitude`
- `cNNOffset`
- `cNNPhase`

## Screen generation

Phoebus screen generator script is in `screens/generate_screen.py`.

Generate screen file:

```bash
python screens/generate_screen.py --title "Siglent SDG" "$(DEV):"
```

This creates `screens/siglent_sdg.bob`.

## Notes

- This module follows the same control-loop structure used by other `epicsdev` device servers.
- SCPI behavior and supported parameter ranges depend on the specific SDG model/firmware.
