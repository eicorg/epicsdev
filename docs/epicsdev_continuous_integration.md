# Building standalone executables for epicsdev PVAccess servers

An epicsdev-based Python PVAccess server can be packaged as a standalone
Linux executable with **PyInstaller**. The executable bundles the Python
interpreter, Python dependencies, and EPICS/PVXS shared libraries. The target
machine does not need Python, `uv`, or an activated virtual environment.

This procedure was verified with the vacuum-controller server
[epicsdev_vac](../epicsdev_vac/README.md). Adapt the package name and
device-specific dependencies when building another server.

## 1. Prepare the project

Build from the project directory containing `pyproject.toml`. The server must
already run successfully from its Python environment, and its runtime
dependencies must be declared in that file.

For the vacuum-controller example, the runtime dependencies are:

```toml
[project]
name = "epicsdev_vac"
version = "0.0.3"
requires-python = ">=3.11"
dependencies = [
    "epicsdev>=3.3.3",
    "pyvisa>=1.14",
    "pyvisa-py>=0.7",
]
```

Add an optional dependency group for executable builds:

```toml
[project.optional-dependencies]
binary = [
    "pyinstaller>=6.16,<7",
    "pyserial>=3.5",
]
```

PySerial is included here because this executable supports direct serial
connections through PyVISA-py. It is not required by every epicsdev server.
If serial support is required in the normal Python installation too, declare
PySerial as a runtime dependency instead.

Install `uv` and `make` on the build machine, then install the build environment:

```sh
uv sync --extra binary
```

Use a project-local environment rather than installing PyInstaller into an
unrelated system environment. `uv run --extra binary` below uses the same
project environment and includes the build dependencies.

## 2. Select the entry point

Use the Python file that starts the server. For this example it is
`epicsdev_vac/__main__.py`, which calls `main()` under this guard:

```python
if __name__ == '__main__':
    main()
```

PyInstaller executes this file as a script. If another server's entry module
uses package-relative imports, use a small launcher at the project root
instead, so the entry module is imported within its package:

```python
from your_server_package.__main__ import main

if __name__ == '__main__':
    main()
```

Pass the launcher filename to PyInstaller in place of the package's
`__main__.py`. Adapt this launcher if the server exposes a differently named
startup function. Do not duplicate the server implementation in the launcher.

## 3. Build the executable

The following command builds the vacuum-controller server:

```sh
uv run --extra binary pyinstaller --noconfirm --clean --onefile \
    --name epicsdev_vac \
    --collect-all pyvisa_py \
    --copy-metadata pyvisa-py \
    --hidden-import serial \
    --collect-binaries epicscorelibs \
    --collect-submodules epicscorelibs.lib \
    --collect-binaries pvxslibs \
    --collect-submodules pvxslibs.lib \
    epicsdev_vac/__main__.py
```

For another epicsdev server, replace `epicsdev_vac` in `--name` and the entry
point path. Keep the EPICS/PVXS collection options. Include only the
device-specific collection options needed by that server.

### Why these options are needed

| Option | Purpose |
| --- | --- |
| `--onefile` | Produce one executable rather than a directory of runtime files. |
| `--name epicsdev_vac` | Set the output filename. |
| `--noconfirm` | Allow replacement of generated output without an interactive prompt. |
| `--clean` | Clear PyInstaller caches and temporary build files before building. |
| `--collect-binaries epicscorelibs` | Bundle the EPICS native shared libraries. |
| `--collect-submodules epicscorelibs.lib` | Include dynamically imported EPICS library metadata modules. |
| `--collect-binaries pvxslibs` | Bundle the PVXS native shared libraries used by p4p. |
| `--collect-submodules pvxslibs.lib` | Include dynamically imported PVXS library metadata modules. |
| `--collect-all pyvisa_py` | Include the pure-Python VISA backend and its dynamically selected modules. |
| `--copy-metadata pyvisa-py` | Preserve the backend's distribution metadata for runtime version lookup. |
| `--hidden-import serial` | Include PySerial for direct serial resources. |

The EPICS metadata options are important: collecting shared libraries alone
is insufficient. An initial build without these submodules failed at startup
with:

```text
ModuleNotFoundError: No module named 'epicscorelibs.lib.ca_dsoinfo'
```

The metadata modules allow `setuptools_dso` to resolve the bundled native
libraries. Keep the analogous PVXS metadata modules as well.

Servers that do not use PyVISA can omit the three VISA/serial options and the
corresponding dependencies. Other dynamically loaded device backends may need
their own hidden imports, package data, or shared-library collection options.
Validate their actual runtime path; a successful build alone does not prove
that every backend has been bundled.

### Repeatable Makefile target

The verified project contains this
[Makefile](../epicsdev_vac/Makefile):

```makefile
.PHONY: executable

executable:
	uv sync --extra binary
	uv run --extra binary pyinstaller --noconfirm --clean --onefile \
		--name epicsdev_vac \
		--collect-all pyvisa_py \
		--copy-metadata pyvisa-py \
		--hidden-import serial \
		--collect-binaries epicscorelibs \
		--collect-submodules epicscorelibs.lib \
		--collect-binaries pvxslibs \
		--collect-submodules pvxslibs.lib \
		epicsdev_vac/__main__.py
```

Recipe lines must begin with a literal tab. Build from the project root:

```sh
make executable
```

PyInstaller writes:

- `dist/epicsdev_vac`: the deployable executable.
- `build/`: intermediate analysis and build output.
- `epicsdev_vac.spec`: the generated build specification.

Only the executable is needed on the target for this one-file build.
Keep generated output out of source control. The vacuum project already
ignores `dist/`, `build/`, and generated `*.spec` files. If a project instead
maintains a customized specification as its build definition, track that
specific file deliberately.

## 4. Verify the bundled runtime

First check that imports and argument parsing work:

```sh
./dist/epicsdev_vac --help
```

This is a startup smoke test, not a test of hardware communication or
PVAccess publication. Follow it with a simulator-based integration test that
starts the **executable**, rather than importing the source module.

The vacuum project provides an opt-in
[executable integration test](../epicsdev_vac/tests/test_executable.py):

```sh
EPICSDEV_VAC_EXECUTABLE="$PWD/dist/epicsdev_vac" \
    uv run --extra binary python -m unittest discover \
    -s tests -p test_executable.py -v
```

The test verifies all three supported models (`BRAX_3000`, `GP307`, and
`GP358`) against local TCP controller simulators. It checks connection health,
pressure and relay readback through a PVAccess client, and clean shutdown.
The executable runs from a temporary working directory with `PYTHONPATH`,
`PYTHONHOME`, and `LD_LIBRARY_PATH` removed, and without the virtual environment
on `PATH`. Python is needed to run the test harness, not the executable itself.

For another server, provide an equivalent test for its transport and
published PVs. Exercise each backend included in the executable. For serial
servers, a pseudo-terminal simulator can verify serial opening and protocol
framing without connecting to real equipment.

The vacuum build was also checked against a pseudo-terminal: its bundled
serial backend opened the ASRL resource and sent the expected native firmware
query, `#  VER\r`.

Do not launch the server with its default resource merely to test packaging.
Without `--help`, it starts the PVAccess server and polls the configured
controller. Use explicit simulator resources during validation.

## 5. Deploy and run

Copy `dist/epicsdev_vac` to the target Linux machine and preserve its executable
permission. It accepts the same arguments as the original module:

```sh
./epicsdev_vac --resource TCPIP0::192.168.27.10::2103::SOCKET --autosave
```

Replace the address and port with the intended controller or gateway.
In this server, bare `--autosave` disables caching. To retain cached PV
values, pass a writable directory instead:

```sh
./epicsdev_vac --resource TCPIP0::192.168.27.10::2103::SOCKET \
    --autosave /path/to/writable/cache
```

Packaging does not change the server's arguments, PV definitions, control
semantics, or hardware-safety requirements. External configuration, caches,
operator displays, and device permissions still need to be managed separately.

### Platform constraints

- Build on Linux for Linux deployment; this is not a cross-platform build.
- Match the target CPU architecture. The verified build is Linux x86-64.
- Build on a Linux distribution with glibc compatible with the target.
  Building on the oldest supported distribution is generally preferable:
  a newer build may require symbols unavailable on an older machine.
- System libraries such as glibc are not bundled. Test on the intended target
  distribution before deployment.
- One-file executables extract their runtime to a temporary directory.
  That directory must be writable and permit loading shared libraries.
  If the default temporary filesystem is unsuitable, set `TMPDIR` to an
  appropriate directory before launching.
- Network access, firewall rules, and serial-device permissions still apply.
- Retain required third-party license notices when distributing the bundle.

The verified vacuum executable was approximately 43 MB. Size depends on the
Python version, dependency versions, and collection options.

## Continuous-integration use

Use the same build and simulator checks in CI. To keep dependencies stable,
generate and track `uv.lock` after updating the manifest. A CI runner can then
use the lock file without updating dependency resolution:

```sh
uv sync --frozen --extra binary
uv run --frozen --extra binary pyinstaller --noconfirm --clean --onefile \
    --name epicsdev_vac \
    --collect-all pyvisa_py \
    --copy-metadata pyvisa-py \
    --hidden-import serial \
    --collect-binaries epicscorelibs \
    --collect-submodules epicscorelibs.lib \
    --collect-binaries pvxslibs \
    --collect-submodules pvxslibs.lib \
    epicsdev_vac/__main__.py
./dist/epicsdev_vac --help
EPICSDEV_VAC_EXECUTABLE="$PWD/dist/epicsdev_vac" \
    uv run --frozen --extra binary python -m unittest discover \
    -s tests -p test_executable.py -v
```

Update the lock file intentionally when dependencies change; `--frozen`
assumes it already matches the intended manifest. Retain the executable as
the release artifact only after validation succeeds. Label artifacts with
the server version, operating system, and architecture, and record the build
environment so compatibility can be assessed later.