"""EPICS PVAccess server of simulated oscilloscope"""
# pylint: disable=invalid-name
__version__= 'v0.2.2 26-01-15'#

import time
import numpy as np
#from p4p.nt import NTScalar, NTEnum
from .epicsdev import printi, printw, printe, printv, printvv, printv3, pvobj, pvv, publish
from .epicsdev import SPV, Server, serverState, init_epicsdev
from .epicsdev import set_server# temporarily

def define_PVs():
    """Define PVs to be published. Return list of PV definitions."""
    SET,U,LL,LH = 'setter','units','limitLow','limitHigh'
    #alarm = {'valueAlarm':{'lowAlarmLimit':0, 'highAlarmLimit':100}}
    n = pargs.npoints
    return [
['dateTime', 'Current date and time', SPV('',R), {}],
['recordLength','Max number of points',     SPV(n,'U32'), W, {SET:set_recordLength}],
['noiseLevel', 'Noise amplitude',  SPV(C_.noiseLevel), W, {SET:set_noise}],
['tAxis', 'Full scale of horizontal axis', SPV([0.]*n), R,  {}],
['c00Waveform', 'Waveform array',   SPV([0.]*n), R, {}],
['c00Peak2Peak', 'Peak to peak value', SPV(0.), R, {}],
]
#``````````````````Setters````````````````````````````````````````````````````
def set_recordLength(value):
    printv(f'>set_recordLength {value}')
    publish('recordLength', value)
    init_peaks() # Re-initialize parameters of peaks and background

#``````````````````Simulated peaks````````````````````````````````````````````
def set_noise(level):
    printv(f'>set_noise {level}')
    C_.noiseLevel = level
    publish('noiseLevel', level)
    #C_.noiseArray = np.random.normal(level, size)

def gaussian(x, sigma):
    """Function, representing gaussian peak shape"""
    return np.zeros(len(x)) if sigma == 0 else np.exp(-0.5*(x/sigma)**2)

RankBkg = 3
def func_sum_of_peaks(xx, *par):
    """Base and sum of peaks."""
    if RankBkg == 3:
        s = par[0] + par[1]*xx + par[2]*xx**2 # if RankBkg = 3
    elif RankBkg == 1:
        s = par[0] # if RankBkg = 1
    for i in range(RankBkg,len(par),3):
        s += par[i+2]*gaussian(xx-par[i],par[i+1])
    return s

def noisyArray(size):
    return np.random.normal(scale=0.5,size=size)

def generate_waveForm():
    """Generate multiple peaks and noise"""
    n = len(C_.timeArray)
    v = func_sum_of_peaks(C_.timeArray, *C_.peaksParameters)
    wf = v + noisyArray(n)*C_.noiseLevel
    return wf

def generate_pars(n):
    #default coeffs for --background
    linmin = 1.
    linmax = 30.
    quadmax = 20.
    a = -4*quadmax/n**2
    b = -a*n + (linmax-linmin)/n
    bckPars = [linmin, round(b,6), round(a,9)]
    peakPars = [0.3*n,0.015*n,10, 0.5*n,0.020*n,40, 0.7*n,0.025*n,15]
    return bckPars + peakPars

def init_peaks():
    """Initialize parameters of peaks and background"""
    recordLength = pvv('recordLength')
    C_.timeArray = np.linspace(0,1,recordLength)
    C_.peaksParameters = generate_pars(recordLength)
    print(f'peaksParameters: {C_.peaksParameters}')

def init(programArguments, pvDefs):
    """Initialization"""
    set_noise(pvv('noiseLevel'))
    init_peaks()
    return pvs

def rareUpdate():
    """Called for infrequent updates"""
    publish('dateTime',time.strftime("%Y-%m-%d %H:%M:%S"))

def poll():
    """Update PVs with new values"""
    #publish('tAxis', C_.timeArray)
    tnow = time.time()
    if tnow - C_.lastRareUpdate > 10.:
        C_.lastRareUpdate = tnow
        rareUpdate()
    cycle = pvv('cycle') + 1
    printv(f'cycle: {pvv("cycle")}')
    publish('cycle', cycle)
    wf = generate_waveForm()
    #printv(f'publish waveform: {wf}')
    publish('c00Waveform', wf)
    publish('c00Peak2Peak', np.ptp(wf))

class C_():
    """Storage for module properties"""
    noiseLevel = 1.0
    timeArray = None
    peaksParameters = None
    lastRareUpdate = 0.

#``````````````````__main__````````````````````````````````````````````````````
if __name__ == "__main__":
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(description = __doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog=f'{__version__}')
    parser.add_argument('-c','--channels', type=int, default=4, help=
'Number of channels in the device.')
    parser.add_argument('-d', '--deviceName', default='simScope', help=
'The PV name will be {deviceName}{deviceIndex}:.')
    parser.add_argument('-e', '--externalControl', default='simScope0', help=
'PV name of the external control. If specified, the server will be controlled by this PV, instead of the default "server" PV.')
    parser.add_argument('-i', '--deviceIndex', type=int, default=0, help=
'Index of the device, if multiple devices are simulated. The master device should have index 0.')
    parser.add_argument('-l', '--listPVs', action='store_true', help=\
'List all generated PVs')
    parser.add_argument('-n', '--npoints', type=int, default=100, help=
        'Max number of points per waveform.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=\
'Show more log messages (-vv: show even more.)')
    pargs = parser.parse_args()

    # Initialize epicsdev and PVs
    prefix = pargs.deviceName + str(pargs.deviceIndex) + ':'
    PVs = init(prefix, define_PVs(), pargs.verbose)
    if pargs.listPVs:
        print('List of PVs:')
        for pvname in pvs:
            print(pvname)

    # Start the Server. Use your set_server, if needed.
    set_server('Start')

    # Main loop
    server = Server(providers=[PVs])
    printi(f'Server started with polling interval {repr(pvv("polling"))} S.')
    while not serverState().startswith('Exit'):
        time.sleep(pvv("polling"))
        if not serverState().startswith('Stop'):
            poll
    printi('Server is exited')