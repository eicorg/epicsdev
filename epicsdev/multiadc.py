"""Simulated multi-channel ADC device server using epicsdev module."""
# pylint: disable=invalid-name
__version__= 'v0.1.0 26-10-02'# Conform to epicsdev 3.3.3+

import sys
import time
from time import perf_counter as timer
import numpy as np
import argparse

#from .epicsdev import  Server, Context, init_epicsdev, serverState, publish
#from .epicsdev import  pvv, printi, printv, set_server, 
from epicsdev import epicsdev as edev

def myPVDefs():
    """Return list of PV definitions"""
    # abbreviations for PV definition dictionary keys
    F, T, U, LL, LH = 'features', 'type', 'units', 'limitLow', 'limitHigh'
    SET = 'setter'
    alarm = {'valueAlarm':{'lowAlarmLimit':-9., 'highAlarmLimit':9.}}

    # Define PVs for the multi-channel ADC server.
    pvDefs = [
#['externalControl', 'Name of external PV, which controls the server',
#    'Start Stop Clear Exit Started Stopped Exited'.split(), {F:'W'}], 
['noiseLevel',  'Noise amplitude', 1.E-4, {SET:set_noise, U:'V'}],
['tAxis',       'Full scale of horizontal axis', [0.], {U:'S'}],
['recordLength','Max number of points', 100,
    {F:'W', T:'u32', LL:4, LH:1000000, SET:set_recordLength}],
['alarm', 'PV with alarm', 0, {F:'WA', U:'du',**alarm}],
    ]

    # Templates for channel-related PVs. Important: SPV cannot be used in this list!
    ChannelTemplates = [
['c0$VoltsPerDiv',  'Vertical scale',       1E-3, {F:'W'}, {U:'V/du'}],
#['c0$VoltOffset',  'Vertical offset',       (1E-3,), {U:'V/du'}],
['c0$Waveform', 'Waveform array',           [0.], {U:'du'}],
['c0$Mean',     'Mean of the waveform',     0., {F:'A', U:'du'}],
['c0$Peak2Peak','Peak-to-peak amplitude',   0., {F:'A', U:'du', **alarm}],
    ]
    # extend PvDefs with channel-related PVs
    for ch in range(pargs.channels):
        for pvdef in ChannelTemplates:
            newpvdef = pvdef.copy()
            newpvdef[0] = pvdef[0].replace('0$',f'{ch+1:02}')
            newpvdef[2] = pvdef[2]
            pvDefs.append(newpvdef)
    return pvDefs

nPatterns = 100 # number of waveform patterns.
pargs = None
rng = np.random.default_rng(nPatterns)
nPoints = 100
verbose = 0

def set_recordLength(value):
    """Record length have changed. The tAxis should be updated accordingly."""
    edev.printi(f'Setting tAxis to {value}')
    edev.publish('tAxis', np.arange(value)*1.E-6)
    edev.publish('recordLength', value)
    set_noise(edev.pvv('noiseLevel')) # Re-initialize noise array, because its size depends on recordLength

def set_noise(level):
    """Noise level have changed. Update noise array."""
    v = float(level)
    recordLength = edev.pvv('recordLength')
    ts = timer()

    pargs.noise = np.random.normal(scale=0.5*level, size=recordLength+nPatterns)# 45ms/1e6 points
    edev.printi(f'Noise array[{len(pargs.noise)}] updated with level {v:.4g} V. in {timer()-ts:.4g} S.')
    edev.publish('noiseLevel', level)

# def set_externalControl(value):
#     """External control PV have changed. Control the server accordingly."""
#     pvname = str(value)
#     if pvname in (None,'0'):
#         edev.printi('External control is not activated.')
#         return
#     edev.printi(f'External control PV: {pvname}')
#     ctxt = edev.Context('pva')
#     try:
#         r = ctxt.get(pvname, timeout=0.5)
#     except TimeoutError:
#         edev.printi(f'Cannot connect to external control PV {pvname}.')
#         sys.exit(1)

def init(recordLength):
    """Testing function. Do not use in production code."""
    set_recordLength(recordLength)
    #set_externalControl(pargs.prefix + pargs.external)

def poll():
    """Example of polling function"""
    #pattern = C_.cycle % nPatterns# produces sliding
    cycle = edev.pvv('cycle')
    edev.printv(f'cycle {repr(cycle)}')
    edev.publish('cycle', cycle + 1)
    for ch in range(pargs.channels):
        pattern = rng.integers(0, nPatterns)
        chstr = f'c{ch+1:02}'
        wf = pargs.noise[pattern:pattern+edev.pvv('recordLength')].copy()
        #print(f'ch{ch}, {pattern}: {wf[0], wf.sum(), wf.mean(), np.mean(wf)}')
        wf /= edev.pvv(f'{chstr}VoltsPerDiv')
        #wf += edev.pvv(f'{chstr}Offset')
        wf += ch
        edev.publish(f'{chstr}Waveform', list(wf))
        edev.publish(f'{chstr}Peak2Peak', np.ptp(wf))
        edev.publish(f'{chstr}Mean', np.mean(wf))

def periodic_update():
    """Function called periodically in the main server loop."""
    edev.printv('Periodic update called.')

# Argument parsing
parser = argparse.ArgumentParser(description = __doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog=f'{__version__}, epicsdev:{edev.__version__}')
parser.add_argument('-a', '--autosave', nargs='?', default='', help=
'Autosave control. If omitted, autosave is enabled with default directory.')
parser.add_argument('-c', '--recall', action='store_false', help=
'If given: do not restore initial PV values from autosave cache.')
parser.add_argument('-C', '--channels', type=int, default=6, help=
'Number of channels per device')
parser.add_argument('-e', '--external', help=
'Name of external PV, which controls the server, if 0 then it will be <device>0:')
parser.add_argument('-l', '--list', default=None, nargs='?', help=
'Directory to save list of all generated PVs, if None, then </tmp/pvlist/><prefix> is assumed.')
parser.add_argument('-i', '--instance', default='0', help=
'Device index, the PV name will be <device><index>:') 
# The rest of arguments are not essential, they can be changed at runtime using PVs.
parser.add_argument('-n', '--npoints', type=int, default=nPoints, help=
'Number of points in the waveform')
parser.add_argument('-p', '--putlogPV', nargs='?', default='', help=
'PV name for logging put operations. Empty means default putlog:dump.')
parser.add_argument('-v', '--verbose', action='count', default=verbose, help=
'Show more log messages (-vv: show even more)') 
parser.add_argument('device', nargs='?', default='multiadc:', help=
'Device name, the prefix for all generated PVs <prefix><instance>:')
pargs = parser.parse_args()
print(f'pargs: {pargs}')

# Initialize epicsdev and PVs
pargs.prefix = f'{pargs.device}{pargs.instance}:'
PVs = edev.init_epicsdev(pargs.prefix, myPVDefs(), pargs.verbose,
    serverStateChanged=None,
    listDir=pargs.list,
    autosaveDir=pargs.autosave,
    recall=pargs.recall,
    putlogPV=pargs.putlogPV)

# Initialize the device, using pargs if needed. That can be used to set the number of points in the waveform, for example.
init(pargs.npoints)

# Start the server and print initial status.
edev.publish('VERSION', __version__)
edev.set_server('Start')
server = edev.Server(providers=[PVs])
edev.printi((f'Server for {pargs.prefix} started. Sleeping per cycle: '
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
