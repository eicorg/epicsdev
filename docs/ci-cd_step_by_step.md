# Development and deployment of epicsdev-based EPICS PVAccess servers
## 1. Development
1) Create repository in github.com/eicorg. Normally the epicdev-based servers have following naming convention:
   epicsdev_hardwareType__manufacturer_model. For example `epicsdev_ps_caen_fastps`.
   - Enable README.md creation.
   - Select License:  BSD 3-Clause.
2) Clone this repository to your local directory.
3) In your directory:
```bash
mkdir my_server opi docs misc
touch my_server/__init__.py

uv init
uv add epicsdev
```
Copy the instrument programming manual to: ```misc/programming_manual.pdf```

Copy the [server template](https://github.com/eicorg/epicsdev/blob/main/docs/template.py) to: ```my_server/__main__.py ```

### Check if basic functionality is working
```bash
uv run python -m my_server
```
Check from another terminal that the server publishes templated PVs:
```bash
pvmonitor template:0:cycle template:0:cycleTime
```
It should print:
```bash
template:0:cycle     2026-10-15 11:04:08.735  61 
template:0:cycleTime 2026-10-15 11:04:08.735  1.00443 
template:0:cycle     2026-10-15 11:04:18.777  71 
template:0:cycleTime 2026-10-15 11:04:18.778  1.00423
... 
```
### Use an AI agent to build the server according to the instrument's programming manual

From the project directory, prompt an AI agent such as GitHub Copilot:

```text
Modify my_server/__main__.py to provide EPICS PVAccess support for <instrument name and model>.
Use the programming manual in misc/programming_manual.pdf as the primary reference.
```

Add relevant details to the prompt to obtain a better targeted result, for example:

- Connection type and address: TCP/IP, USB, serial, or GPIB
- Required instrument functions and parameters
- Preferred EPICS PV naming convention
- Polling rate and performance requirements
- Required OPI screens or example configuration

Review the agent’s recommendations, test the server with the real instrument, and refine error handling and recovery behavior as needed.

### Test run
```
uv run python -m my_server
```
## 2. Deployment
To package epicsdev-based PVAccess servers as standalone Linux executables in your build pipeline, 
you can ask the AI agent to build an executable from your repository. It will take approximately 5 minutes.

The generated executable encapsulates everything, the typical size is ~ 50MB.

For behind-the-scene procedure 
see the [Continuous Integration Guide](docs/epicsdev_continuous_integration.md).
