# epicsdev
EPICS PVAccess servers for various instruments

## Simulated instriments:<br>
###multiadc: Multi-channel waveform generator
Module **epicdev.multiadc** can generate large amount of data for stress-testing
the EPICS environment. For example the following command will generate 100 of 
1000-pont noisy waveforms and 300 of scalar parameters.
```
python -m epicsdev.multiadc -c100 -n1000
```

## Oscilloscope series
- RIGOL DHO
- TEKTRONIX MSO
- LECROY WAVERUNNER
- KEYSIGHT (AGILENT) DSO-X

## Magnetometers
- LAKESHORE (model 421)

## DAQ


