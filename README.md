# epicsdev

`epicsdev` is a Python framework for rapidly developing EPICS PVAccess servers with the [p4p](https://github.com/epics-base/p4p) library.

Device PVs are specified as a compact list of ```[name, description, initial_value, attributes]```tuples. 
The framework automatically creates the server, performs periodic updates, and implements standard EPICS services: **autosave/restore, IocStats, heartbeat monitoring, and PV-put logging**.

Device-specific logic is contained in a small, well-structured Python file that follows a predictable pattern. Given an instrument programming manual, a large language model (LLM) assistant such as GitHub Copilot can use this pattern to create initial support for a new instrument quickly.

## Automatic generation of PVAccess server and OPI display

Follow these [detailed instructions](docs/generate_server.md) to generate a functional PVAccess server supporting the instrument's basic functions. Initial implementation can often be completed within an hour.

An Operator Interface (OPI) display can also be generated automatically with [phoebusgen](https://als-epics.github.io/phoebusgen/). 
See [this instructions](docs/generate_opi.md).

## Available device support

Power supplies
- [CAEN FAST-PS](https://github.com/eicorg/epicsdev_ps_caen_fastps)
- [CAEN EASY-DRIVER](https://github.com/eicorg/epicsdev_ps_caen_easydriver)

Oscilloscopes
- [Keysight (Agilent) DSO-X series](https://github.com/eicorg/epicsdev_osc_keysight_dsox)
- [Rigol DHO series](https://github.com/eicorg/epicsdev_osc_rigol)
- [Tektronix MSO and DPO series](https://github.com/eicorg/epicsdev_osc_tektronix_mso)
- [LeCroy WaveRunner series](https://github.com/eicorg/epicsdev_osc_lecroy_waverunner)

Signal generators

- [Siglent SDG series](https://github.com/eicorg/epicsdev_siggen_siglent_sdg)
- [Keysight 33000 series](https://github.com/eicorg/epicsdev_siggen_keysight_33000)

Data-acquisition systems
- [CAEN DT5202](https://github.com/eicorg/epicsdev_daq_caen_dt5202)
- [LabJack U3](https://github.com/eicorg/epicsdev_daq_labjack_u3)

Magnetometers
- [Lake Shore Model 421](https://github.com/eicorg/epicsdev_magn_lakeshore)

Simulated instruments
- [Multi-channel waveform generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/multiadc.py)

  For example, the following command generates 100 noisy waveforms, each with 1,000 points, and 300 scalar parameters:

  ```bash
  python -m epicsdev.multiadc -c100 -n1000
  ```

- [Multi-peak image generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/imagegen.py)
