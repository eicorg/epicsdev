# epicsdev

`epicsdev` is a Python framework designed for rapidly developing EPICS PVAccess servers using the [p4p](https://github.com/epics-base/p4p) library.

Device process variables (PVs) are defined using a compact format:
```python
[name, description, initial_value, attributes]
```

Device-specific logic resides within a small, well-structured Python file following a predictable pattern. Given an instrument programming manual, an LLM assistant (such as GitHub Copilot) can easily leverage this pattern to spin up initial support for new hardware in under an hour.

---

## Key Features

* **High-Bandwidth Data Streaming:** Minimizes packet overhead and uses the optimized p4p bindings to move complex data structures directly.
* **Built-in Services:** Out-of-the-box support for autosave/restore, IocStats, heartbeat monitoring, and PV-put logging.
* **Rapid Prototyping:** Simple, declarative format for PV definitions.
* **LLM-Friendly:** Highly predictable boilerplate that allows AI code assistants to write drivers effortlessly.
* **OPI Integration:** Automated operator interface generation for Phoebus.

---

## Getting Started

### 1. Generate a PVAccess Server
Follow the [Detailed Server Generation Guide](docs/generate_server.md) to bootstrap a functional PVAccess server supporting your instrument's core functions.

### 2. Generate an OPI Display
You can automatically create an operator interface (OPI) layout using [phoebusgen](https://als-epics.github.io/phoebusgen/). See the [OPI Generation Instructions](docs/generate_opi.md) for details.

### 3. Quick Test (Simulation Mode)
To see the framework in action without physical hardware, you can launch a simulated multi-channel waveform generator, which can be useful for stress-testing EPICS installations. The following command generates 100 noisy waveforms (1,000 points each) alongside 300 scalar parameters:

```bash
python -m epicsdev.multiadc -C 100 -n 1000
```
To change the data publication frequency, modify the `sleep` PV: `pvput multiadc:0:sleep .1`.

#### Quick GUI
To control and plot the server's PVs, you can use the `pypeto` and `pvplot` modules.

```bash
pip install pypeto pvplot
python -m pypeto -f config/multiadc_pp
```

Other examples include a single-waveform generator and a multi-peak image generator:
```bash
python -m epicsdev.epicsdev
python -m epicsdev.imagegen
```
See [imagegen usage](docs/imagegenUsage.md) for more details.

### 4. Continuous Integration
To package `epicsdev`-based PVAccess servers as standalone Linux executables in your build pipeline, see the [Continuous Integration Guide](docs/epicsdev_continuous_integration.md) for PyInstaller build instructions and dependency requirements.

## Fully Functional PVAccess Servers Developed Using epicsdev

Power Supplies
* [CAEN FAST-PS](https://github.com/eicorg/epicsdev_ps_caen_fastps)
* [CAEN EASY-DRIVER](https://github.com/eicorg/epicsdev_ps_caen_easydriver)

Oscilloscopes
* [Keysight (Agilent) DSO-X series](https://github.com/eicorg/epicsdev_osc_keysight_dsox)
* [Rigol DHO series](https://github.com/eicorg/epicsdev_osc_rigol)
* [Tektronix MSO and DPO series](https://github.com/eicorg/epicsdev_osc_tektronix_mso)
* [LeCroy WaveRunner series](https://github.com/eicorg/epicsdev_osc_lecroy_waverunner)

Signal Generators
* [Siglent SDG series](https://github.com/eicorg/epicsdev_siggen_siglent_sdg)
* [Keysight 33000 series](https://github.com/eicorg/epicsdev_siggen_keysight_33000)

Data Acquisition Instruments
* [CAEN DT5202](https://github.com/eicorg/epicsdev_daq_caen_dt5202)
* [NI cDAQ](https://github.com/eicorg/epicsdev_cdaq). Under development
* [LabJack U3](https://github.com/eicorg/epicsdev_daq_labjack_u3)

Magnetometers
* [Lake Shore Model 421](https://github.com/eicorg/epicsdev_magn_lakeshore)
* [Caylar NMR20](https://github.com/eicorg/epicsdev_magn_caylar_nmr)

Vacuum Gauge Controllers
* [Granville-Phillips 307 and 358](https://github.com/eicorg/epicsdev_vac)
* [B-RAX 3000 series](https://github.com/eicorg/epicsdev_vac) from InstruTech

Simulation Utilities
* [Multi-channel Waveform Generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/multiadc.py)
* [Multi-peak Image Generator](https://github.com/eicorg/epicsdev/blob/main/epicsdev/imagegen.py)
