"""EPICS PVAccess server for template."""
# pylint: disable=invalid-name,broad-exception-caught
__version__ = 'v0.0.2 2026-10-01'# --index replaced with --instance. This is more generic.

import argparse
from dataclasses import dataclass

from epicsdev import epicsdev as edev

DEVICE = 'template:'

#````````````````````````````````````````````````````````````````````````````
# Definitions of PVs, their types, units, limits, and setter functions are
# defined in the myPVDefs() function below.
def myPVDefs():
    """Return list of PV definitions"""
    # abbreviations for PV definition dictionary keys
    F, T, U, LL, LH = 'features', 'type', 'units', 'limitLow', 'limitHigh'
    SET = 'setter'

    pv_defs = [
['dateTime', 'Server local date/time', 'N/A'],
    # TODO: add your PV definitions here
    ]
    return pv_defs
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

@dataclass(slots=True)
class C_:
    """Container for module state variables."""
    pargs = None #

def poll():
    """Poll for updates from the hardware or other sources."""
    # TODO: implement polling logic

def periodic_update():
    """Perform periodic updates."""
    # TODO: implement periodic update logic

def serverStateChanged(newState: str):
    """Callback for server state transitions."""
    if newState == 'Start':
        edev.printi('Start requested')
    elif newState == 'Stop':
        edev.printi('Stop requested')
    elif newState == 'Exit':
        edev.printi('Exit requested')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f'{__version__}, epicsdev:{edev.__version__}',
    )
    # commonly used options
    parser.add_argument('-a', '--autosave', nargs='?', default='', help=
'Autosave control. If omitted, autosave is enabled with default directory.')
    parser.add_argument('-c', '--recall', action='store_false', help=
'If given: do not restore initial PV values from autosave cache.')
    parser.add_argument('-i', '--instance', default='0', help=
'Device instance.')
    parser.add_argument('-p', '--putlogPV', nargs='?', default='', help=
'PV name for logging put operations. Empty means default putlog:dump.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=
'Increase verbosity (-vv for more).')
    parser.add_argument('device', nargs='?', default=DEVICE, help=
'Device name, the prefix for all generated PVs <prefix><instance>:')

    # TODO: add your options here
    
    # Parse command-line arguments and store them in the module state container.
    C_.pargs = parser.parse_args()
    if C_.pargs.putlogPV == '':
        C_.pargs.putlogPV = 'putlog:dump'
    C_.pargs.prefix = f'{C_.pargs.device}{C_.pargs.instance}:'

    # Initialize PV definitions.
    C_.PvDefs = myPVDefs()

    # Initialize the EPICS PVAccess server with the defined PVs.
    PVs = edev.init_epicsdev(
        C_.pargs.prefix,
        C_.PvDefs,
        C_.pargs.verbose,
        serverStateChanged,
        '',
        C_.pargs.autosave,
        C_.pargs.recall,
        C_.pargs.putlogPV,
    )
    print(f'Using PV prefix: {C_.pargs.prefix}')

    # Start the server and print initial status.
    edev.publish('VERSION', __version__)
    edev.set_server('Start')
    server = edev.Server(providers=[PVs])
    edev.printi((f'Server for {C_.pargs.prefix} started. Sleeping per cycle: '
                 f'{repr(edev.pvv("sleep"))} S.'))

    # Main server loop. Polls for updates and handles server state transitions.
    try:
        while True:
            state = edev.serverState()
            if state.startswith('Exit'):
                break
            if not state.startswith('Stop'):
                poll()
            if not edev.sleep():
                periodic_update()
    except KeyboardInterrupt:
        edev.printi('Keyboard interrupt received, exiting main loop...')
        edev.set_server('Exit')
    except OSError:
        pass

    edev.printi('Server is exited')
