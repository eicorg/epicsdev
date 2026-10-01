# epicsdev
Python framework that dramatically reduces the effort required 
to create EPICS PVAccess servers using p4p library.
Device PVs are described  as a compact list of 
`[name, description, initial_value, attributes]` tuples.  

The framework handles server creation, periodic updates, autosave/restore,  
IocStats heartbeat, and PV-put logging automatically. 

Because all device logic lives in a small, well-structured Python file with a  
predictable pattern, large-language-model (LLM) assistants such as GitHub 
Copilot can replicate that pattern for any new instruments given only a  
manufacturer's programming manual.

## Automatic generation of PVAccess server and OPI display.
Using following [detailed instruction](docs.generate_server.md) the development of functional server, 
supporting basic instrument functions could be implemented in a matter of an hour.

The OPI (Operator Interface) display could also be generated automatically using phoebusgen:
[instructions](docs.generate_server.md).

## Device support for following instruments have been developed:
Power Supplies:
- [CAEN FAST-PS](https://github.com/eicorg/epicsdev_ps_caen_fastps)
- [CAEN EASY-DRIVER](https://github.com/eicorg/epicsdev_ps_caen_easydriver)

Oscilloscope series:
- [KEYSIGHT (AGILENT) DSO-X](https://github.com/eicorg/epicsdev_osc_keysight_dsox)
- [RIGOL DHO](https://github.com/eicorg/epicsdev_osc_rigol)
- [TEKTRONIX MSO & DPO](https://github.com/eicorg/epicsdev_osc_tektronix_mso)
- [LECROY WAVERUNNER](https://github.com/eicorg/epicsdev_osc_lecroy_waverunner)

Signal generators:
- [SIGLENT SDG series](https://github.com/eicorg/epicsdev_siggen_siglent_sdg)
- [KEYSIGHT 33000 series](https://github.com/eicorg/epicsdev_siggen_keysight_33000)

Data acquisition systems:
- [CAEN DT5202](https://github.com/eicorg/epicsdev_daq_caen_dt5202)
- [Labjack U3](https://github.com/eicorg/epicsdev_daq_labjack_u3)

Magnetometers:
- [LAKESHORE (model 421)](https://github.com/eicorg/epicsdev_magn_lakeshore)

Simulated instruments:
- [Multi-channel waveform generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/multiadc.py)
For example the following command will generate 100 of 
1000-pont noisy waveforms and 300 of scalar parameters:
```python -m epicsdev.multiadc -c100 -n1000```.
- [Multi-peak image generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/imagegen.py).

