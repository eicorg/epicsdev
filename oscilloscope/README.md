# Oscilloscope servers

This folder contains EPICS PVAccess servers for oscilloscope families, implemented with `epicsdev` and VISA/SCPI.

## Available servers

- Keysight / Agilent DSO-X: [oscilloscope/keysight_dsox](oscilloscope/keysight_dsox). Final release.
- LeCroy WaveRunner / MAUI-family: [oscilloscope/lecroy_waverunner](oscilloscope/lecroy_waverunner). Beta release.
- Rigol DHO: [oscilloscope/rigol_dho](oscilloscope/rigol_dho). Beta release.
- Tektronix MSO (4/5/6 series): [oscilloscope/tektronix_mso](oscilloscope/tektronix_mso). Beta release.

## Common behavior

All servers follow the same high-level pattern:

- connect to instrument via VISA resource
- expose writable/readback PVs for acquisition, trigger, timebase, and per-channel settings
- publish waveform arrays and scalar statistics
- run control loop via `epicsdev` (`server`, `sleep`, autosave, putlog)

Typical PV groups:

- global: `scopeIDN` or `genIDN`, `dateTime`, `server`, `sleep`, `status`
- trigger/timebase: `trigSource`, `trigMode`, `trigLevel`, `timePerDiv`, `samplingRate`
- per-channel: enable/coupling/scale/offset and waveform/statistics PVs

## Quick start

Start a specific server by entering its package directory and running its module, for example:

- Keysight DSO-X: `python -m keysight_dsox`
- LeCroy: `python -m lecroy_waverunner`
- Rigol: `python -m rigol_dho`
- Tektronix: `python -m tektronix_mso`

Then open the corresponding GUI/screen config from each server package.

## Screen generation

Latest servers include Phoebus `.bob` generator scripts in their `screens/` subfolder.

Examples:

- Keysight DSO-X screen generator: [oscilloscope/keysight_dsox/screens/generate_simplescope.py](oscilloscope/keysight_dsox/screens/generate_simplescope.py)

## Notes

- VISA resource strings and SCPI capability vary by model/firmware.
- For model-specific options, defaults, and examples, use each server’s README in its own folder.
