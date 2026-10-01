## Generate the Operator Interface (OPI)

Copy this [OPI generator template](https://github.com/eicorg/epicsdev/blob/main/docs/generate_opi.py) to:

```text
opi/generate_opi.py
```

Then prompt an AI agent such as GitHub Copilot:

```text
Modify opi/generate_opi.py to generate an OPI for the PVs defined in my_server/__main__.py.
```

Include any display-specific requirements in the prompt, such as the desired layout, grouping of controls and readbacks, plots, alarms, or status indicators.
