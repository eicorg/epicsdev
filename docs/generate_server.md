## Automatically generate a PVAccess server for an instrument

### Initialize the project

```bash
mkdir my_server
cd my_server

mkdir my_server opi docs misc
touch my_server/__init__.py

uv init
uv add epicsdev
```

Copy the instrument programming manual to: ```misc/programming_manual.pdf```

Copy the [server template](https://github.com/eicorg/epicsdev/blob/main/docs/template.py) to: ```my_server/__main__.py ```

### Use an AI agent

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

