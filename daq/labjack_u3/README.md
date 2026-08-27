# labjack_u3

EPICS PVAccess server for a LabJack U3 device, implemented with `epicsdev`.

Main server entry point: [labjack_u3/__main__.py](labjack_u3/__main__.py)  
Phoebus screen generator: [screens/generate_screen.py](screens/generate_screen.py)

## Features

- U3 initialization and I/O configuration from `FIO`/`EIO` strings
- Analog readback:
	- `AIN_HV` (high-voltage analog inputs)
	- `AIN_LV` (low-voltage analog inputs)
- Analog outputs:
	- `DAC0`, `DAC1`
- Digital I/O read/write (`DIO*`), based on configured digital channels
- Pulse helpers:
	- `Pulse` selector
	- `PulseFIO*Pars` / `PulseEIO*Pars`
	- `pulseTick`
- PWM controls:
	- `PWM_period`, `PWM_multiplier`, `PWM_pulseWidth`
- Runtime/status:
	- `server`, `sleep`, `hardPoll`, `dateTime`, `tempU3`, `rps`

## Requirements

- Python 3.10+
- `epicsdev`
- `p4p`
- `LabJackPython` (module `u3`)
- `phoebusgen` (for screen generation)

## Run the server

Typical usage:

- `python -m labjack_u3`

Useful options:

- `-d, --device` device prefix base (default: `labjacku3_`)
- `-i, --index` device index (default: `0`)
- `--fio` FIO configuration string (default: `AAAAaDTC`)
- `--eio` EIO configuration string (default: `aaaaDDDD`)
- `-v` increase verbosity

Example:

- `python -m labjack_u3 -d labjacku3_ -i 0 --fio AAAAaDTC --eio aaaaDDDD -v`

Default PV prefix becomes:

- `labjacku3_0:`

## FIO/EIO configuration

Character codes used in `--fio` and `--eio`:

- `A` = high-voltage analog input
- `a` = low-voltage analog input
- `D` = digital I/O
- `T` = timer
- `C` = counter

Only channels configured as digital are exposed as `DIO*` PVs.

## Generate a Phoebus screen

Generate `.bob` file:

- `python screens/generate_screen.py`

Optional arguments:

- `-t, --title` screen title
- `prefix` PV prefix macro/value (default: `$(DEV):`)

Example:

- `python screens/generate_screen.py -t "LabJack U3" "$(DEV):"`

Output file:

- [screens/labjack_u3.bob](screens/labjack_u3.bob)

## Notes

- If `LabJackPython` is missing, startup exits with an error.
- The server uses the standard `epicsdev` control PVs (`server`, `sleep`, autosave/recall integration, put logging).
