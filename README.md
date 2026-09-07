# epicsdev
Python framework that dramatically reduces the effort required 
to create EPICS PVAccess servers using p4p library.
Device support for following instruments have been developed:

## Power Supplies
- [CAEN FAST-PS](https://github.com/eicorg/epicsdev_ps_caen_fastps)

## Oscilloscope series
- [KEYSIGHT (AGILENT) DSO-X](https://github.com/eicorg/epicsdev_osc_keysight_dsox)
- [RIGOL DHO](https://github.com/eicorg/epicsdev_osc_rigol)
- [TEKTRONIX MSO](https://github.com/eicorg/epicsdev_osc_tektronix_mso)
- [LECROY WAVERUNNER](https://github.com/eicorg/epicsdev_osc_lecroy_waverunner)

## Signal generators
- [SIGLENT SDG series](https://github.com/eicorg/epicsdev_siggen_siglent_sdg)
- [KEYSIGHT 33000 series](https://github.com/eicorg/epicsdev_siggen_keysight_33000

## DAQ
- [CAEN DT5202](https://github.com/eicorg/epicsdev_daq_caen_dt5202)
- [Labjack U3](https://github.com/eicorg/epicsdev_daq_labjack_u3)

## Magnetometers
- [LAKESHORE (model 421)](https://github.com/eicorg/epicsdev_magn_lakeshore)

## Simulated instruments<br>
Multi-channel waveform generator:<br>
Module **epicdev.multiadc** can generate large amount of data for stress-testing
the EPICS environment. For example the following command will generate 100 of 
1000-pont noisy waveforms and 300 of scalar parameters:
```python -m epicsdev.multiadc -c100 -n1000```.

