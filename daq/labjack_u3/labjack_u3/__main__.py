"""EPICS PVAccess server for LabJack U3 device."""
# pylint: disable=invalid-name,broad-exception-caught
__version__ = 'v0.0.3 26-08-28'#
#TODO: Handle input IO. Probably need fast loop for reading inpput IO.
#TODO: Check Pulse width, it fails when width is > 7000
#TODO: Check PWM.

import argparse
from functools import partial
import sys
import time

from epicsdev import epicsdev as edev

try:
    import u3
except ModuleNotFoundError:
    u3 = None

ModBusAddr = {'DAC0': 5000, 'DAC1': 5002}
ConfigFIO_desc = (
    'Configuration of FIO and EIO ports. '
    'Codes: A:AIN_HV, a:AIN_LV, D:digital, T:timer, C:counter'
)
DEFAULT_CONFIG_FIO = {'FIO': 'AAAAaDTC', 'EIO': 'aaaaDDDD'}

pargs = None

class C_:
    """Namespace for module state."""

    D = None
    PvDefs = []
    AIN_HVs = []
    AIN_LVs = []
    DIO_read_cmds = []
    DIO_io_numbers = []
    Counter_cmds = []
    counterValues = []
    timerCounterPinOffset = 0
    numberOfTimersEnabled = 0
    last_hw_read = 0.0
    ain_prev_values = []

def _parse_config_fio(config_fio):
    """Build U3 feedback command lists from FIO/EIO configuration strings."""
    C_.AIN_HVs = []
    C_.AIN_LVs = []
    C_.DIO_read_cmds = []
    C_.DIO_io_numbers = []
    C_.Counter_cmds = []

    fio_ain_mask = 0
    eio_ain_mask = 0
    enable_counter = [False, False]
    n_counters = 0
    C_.timerCounterPinOffset = 0
    C_.numberOfTimersEnabled = 0

    for i, ch in enumerate(config_fio['FIO']):
        if ch == 'a':
            fio_ain_mask |= 1 << i
            C_.AIN_LVs.append(u3.AIN(i, NegativeChannel=31, LongSettling=False, QuickSample=True))
        elif ch == 'A':
            fio_ain_mask |= 1 << i
            C_.AIN_HVs.append(u3.AIN(i, NegativeChannel=31, LongSettling=False, QuickSample=True))
        elif ch == 'T':
            if C_.timerCounterPinOffset == 0:
                C_.timerCounterPinOffset = i
            C_.numberOfTimersEnabled += 1
        elif ch == 'C':
            idx = C_.numberOfTimersEnabled + n_counters
            if idx < 2:
                enable_counter[idx] = True
                C_.Counter_cmds.append(u3.Counter(i, Reset=False))
                n_counters += 1
        elif ch == 'D':
            C_.DIO_read_cmds.append(u3.BitStateRead(i))
            C_.DIO_io_numbers.append(i)

    for i, ch in enumerate(config_fio['EIO']):
        io_num = i + 8
        if ch == 'a':
            eio_ain_mask |= 1 << i
            C_.AIN_LVs.append(u3.AIN(io_num, NegativeChannel=31, LongSettling=False, QuickSample=True))
        elif ch == 'D':
            C_.DIO_read_cmds.append(u3.BitStateRead(io_num))
            C_.DIO_io_numbers.append(io_num)

    C_.D.configIO(
        FIOAnalog=fio_ain_mask,
        EIOAnalog=eio_ain_mask,
        TimerCounterPinOffset=C_.timerCounterPinOffset,
        NumberOfTimersEnabled=C_.numberOfTimersEnabled,
        EnableCounter0=enable_counter[0],
        EnableCounter1=enable_counter[1],
    )

def pulse(io_number=5, duration=1, delay=0, positive=True):
    """Pulse a digital IO in 128 us ticks."""
    w_del = divmod(int(delay), 256)
    w_dur = divmod(int(duration), 256)
    cmdlist = [
        u3.WaitLong(w_del[0] * 2),
        u3.WaitShort(w_del[1]),
        u3.BitStateWrite(int(io_number), int(bool(positive))),
    ]
    if duration >= 0:
        cmdlist += [
            u3.WaitLong(w_dur[0] * 2),
            u3.WaitShort(w_dur[1]),
            u3.BitStateWrite(int(io_number), int(not bool(positive))),
        ]
    C_.D.getFeedback(*cmdlist)

def handle_exception(where):
    edev.printe(f'{where}: {sys.exc_info()[1]}')

def _set_dac(par_name, value, *_):
    try:
        v = float(value)
        print(f'Setting {par_name} to {v}')
        C_.D.writeRegister(ModBusAddr[par_name], v)
        edev.publish(par_name, v, ifChanged=True)
    except Exception:
        handle_exception(f'in _set_dac({par_name})')

def _set_do(io_number, value, pv, *_):
    try:
        v = int(float(value))
        C_.D.getFeedback(u3.BitStateWrite(int(io_number), v))
        edev.publish(str(pv.name), v, ifChanged=True)
    except Exception:
        handle_exception(f'in _set_do({io_number})')

def set_pulse(value, *_):
    try:
        pulse_name = str(value)
        pars = edev.pvv(f'{pulse_name}Pars')
        print(f'Setting pulse parameters for {pulse_name} to {pars}')
        pulse(io_number=int(pars[0]), duration=int(pars[1]), delay=int(pars[2]), positive=bool(int(pars[3])))
        edev.publish('Pulse', pulse_name, ifChanged=True)
    except Exception:
        handle_exception('in set_pulse')

def set_pwm(value, *_):
    try:
        multiplier = max(1, int(edev.pvv('PWM_multiplier')))
        pulse_width_ms = float(value)
        print(f'Setting PWM with multiplier={multiplier}, pulse_width_ms={pulse_width_ms, type(pulse_width_ms)}')
        base_value = 65535
        if pulse_width_ms <= 0:
            edev.printi('Turning off PWM')
        C_.D.configTimerClock(TimerClockBase=3, TimerClockDivisor=multiplier)
        ticks = round((pulse_width_ms * 1000.0) / multiplier)
        ticks = max(0, min(base_value, ticks))
        C_.D.getFeedback(u3.Timer0Config(TimerMode=0, Value=base_value - ticks))
    except Exception:
        handle_exception('in set_pwm')

def _set_pulsePars(pulse_name, value, *_):
    print(f'Setting pulse parameters for {pulse_name} to {value}')
    set_pulse(pulse_name)

def myPVDefs():
    F, T, U, LL, LH, SET = 'features', 'type', 'units', 'limitLow', 'limitHigh', 'setter'

    n_hv = len(C_.AIN_HVs)
    n_lv = len(C_.AIN_LVs)
    n_cnt = len(C_.Counter_cmds)
    dac0 = round(C_.D.readRegister(ModBusAddr['DAC0']), 4)
    dac1 = round(C_.D.readRegister(ModBusAddr['DAC1']), 4)
    print(f'DAC0={dac0}, DAC1={dac1}, n_hv={n_hv}, n_lv={n_lv}, n_cnt={n_cnt}')

    pv_defs = [
        ['dateTime', 'Server local date/time', 'N/A'],
        ['DAC0', 'DAC 0.04-4.95V, 10-bit PWM-based', dac0,
            {F: 'W', U: 'V', LL: 0.0, LH: 4.95, SET: partial(_set_dac, 'DAC0')}],
        ['DAC1', 'DAC 0.04-4.95V, 10-bit PWM-based', dac1,
            {F: 'W', U: 'V', LL: 0.0, LH: 4.95, SET: partial(_set_dac, 'DAC1')}],
        ['AIN_HV', '12-bit ADCs. range -10:+10 V', [0.0] * n_hv, {U: 'V'}],
        ['AIN_LV', '12-bit ADCs. range 0:+2.44 V', [0.0] * n_lv, {U: 'V'}],
    ]

    pulse_legal = []
    for io_num in C_.DIO_io_numbers:
        pv_defs.append([
            f'DIO{io_num}',
            f'Digital IO state for U3 IO {io_num}',
            0,
            {F: 'W', T: 'u8', LL: 0, LH: 1, SET: partial(_set_do, io_num)},
        ])
        pulse_name = f'PulseIO{io_num}'
        pulse_legal.append(pulse_name)
        pv_defs.append([
            f'{pulse_name}Pars',
            f'Pulse parameters: ioNumber, duration(-1 infinite), delay, positive for IO {io_num}',
            [io_num, 1000, 0, 1],
            {F: 'W', SET: partial(_set_pulsePars, pulse_name)},
        ])

    if not pulse_legal:
        pulse_legal = ['PulseFIO5']
        pv_defs.append(['PulseFIO5Pars', 'Pulse parameters fallback', [5, 1000, 0, 1], {F: 'W'}])

    pv_defs += [
        ['pulseTick', 'The time resolution of pulse parameters', 0.000128, {U: 's'}],
        ['Pulse', 'Trigger a pulse with selected pulse parameters', pulse_legal, {F: 'WD', SET: set_pulse}],
        ['Count', '32-bit counters, accumulated during polling period', [0] * n_cnt],
        ['frequency', 'Frequency of the counters', [0.0] * n_cnt, {U: 'Hz'}],
        ['PWM_period', 'Period of PWM, 2^16/1MHz', 65.535, {U: 'ms'}],
        ['PWM_multiplier', 'Multiplier of PWM period', 1,
            {F: 'W', T: 'u16', LL: 1, LH: 255, SET: set_pwm}],
        ['PWM_pulseWidth', 'Pulse width of PWM, if <=0 then PWM is off', 0.,
            {F: 'W', U: 'ms', LL: 0.0, LH: 65535.0, SET: set_pwm}],
        ['configFIO', ConfigFIO_desc, str(pargs.configFIO)],
        ['tempU3', 'Temperature of the U3 box', 0.0, {U: 'C'}],
    ]
    return pv_defs

def _read_hardware():
    try:
        cmd = C_.AIN_HVs + C_.AIN_LVs + C_.DIO_read_cmds + C_.Counter_cmds
        if not cmd:
            return

        bits = C_.D.getFeedback(*cmd)
        ts = time.time()
        #print(f'_read_hardware: bits={bits}')
        n_hv = len(C_.AIN_HVs)
        n_lv = len(C_.AIN_LVs)
        n_dio = len(C_.DIO_read_cmds)
        ain_cnt = n_hv + n_lv

        ain_values = []
        for i in range(ain_cnt):
            v = C_.D.binaryToCalibratedAnalogVoltage(
                bits[i],
                isLowVoltage=(i >= n_hv),
                isSingleEnded=True,
                isSpecialSetting=False,
                channelNumber=i,
            )
            ain_values.append(round(v, 5))

        if ain_values != C_.ain_prev_values:
            C_.ain_prev_values = ain_values
            edev.publish('AIN_HV', ain_values[:n_hv], t=ts)
            edev.publish('AIN_LV', ain_values[n_hv:n_hv + n_lv], t=ts)

        dio_vals = bits[ain_cnt:ain_cnt + n_dio]
        for io_num, value in zip(C_.DIO_io_numbers, dio_vals):
            edev.publish(f'DIO{io_num}', int(value), ifChanged=True, t=ts)

        cnt_vals = bits[ain_cnt + n_dio:ain_cnt + n_dio + len(C_.Counter_cmds)]
        freq = []
        edev.publish('Count', [int(v) for v in cnt_vals], ifChanged=True, t=ts)
        for i,count in enumerate(cnt_vals):
            freq.append((count - C_.conterValues[i]) / (ts - C_.last_hw_read) if C_.last_hw_read > 0 else 0.0)
        edev.publish('frequency', freq, ifChanged=True, t=ts)
    except Exception:
        handle_exception('in _read_hardware')
    C_.last_hw_read = ts
    C_.conterValues = cnt_vals

def serverStateChanged(newState: str):
    if newState == 'Start':
        edev.printi('Start requested')
    elif newState == 'Stop':
        edev.printi('Stop requested')
    elif newState == 'Exit':
        edev.printi('Exit requested')

def poll():
    now = time.time()
    _read_hardware()

def periodic_update():
    try:
        edev.publish('tempU3', round(C_.D.getTemperature() - 273.0, 3), ifChanged=True)
    except Exception:
        handle_exception('reading U3 temperature')

def init_u3():
    if u3 is None:
        edev.printe('LabJackPython is not installed. Please install package LabJackPython.')
        sys.exit(1)

    try:
        C_.D = u3.U3()
        _parse_config_fio(pargs.configFIO)
        edev.printi(
            f'Connected to U3 SN:{C_.D.serialNumber} FW:{C_.D.firmwareVersion} '
            f'configFIO:{pargs.configFIO}'
        )
    except Exception:
        handle_exception('initializing LabJack U3')
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=__version__,
    )
    parser.add_argument(
        '-a', '--autosave', nargs='?', default='',
        help='Autosave control. If not given, autosave is enabled with default directory.',
    )
    parser.add_argument(
        '-c', '--recall', action='store_false',
        help='If given: do not restore initial PV values from autosave cache.',
    )
    parser.add_argument(
        '-d', '--device', default='labjacku3_',
        help='Device name, the PV prefix is <device><index>:',
    )
    parser.add_argument(
        '-i', '--index', default='0',
        help='Device index, the PV prefix is <device><index>:',
    )
    parser.add_argument(
        '-p', '--putlogPV', nargs='?', default='',
        help='PV name for logging put operations. Empty means default putlog:dump.',
    )
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity (-vv for more).')
    parser.add_argument('--fio', default=DEFAULT_CONFIG_FIO['FIO'], help='FIO configuration string, e.g. AAAAaDTC')
    parser.add_argument('--eio', default=DEFAULT_CONFIG_FIO['EIO'], help='EIO configuration string, e.g. aaaaDDDD')

    pargs = parser.parse_args()
    pargs.configFIO = {'FIO': pargs.fio, 'EIO': pargs.eio}
    if pargs.putlogPV == '':
        pargs.putlogPV = 'putlog:dump'

    pargs.prefix = f'{pargs.device}{pargs.index}:'
    init_u3()
    C_.PvDefs = myPVDefs()

    PVs = edev.init_epicsdev(
        pargs.prefix,
        C_.PvDefs,
        pargs.verbose,
        serverStateChanged,
        '',
        pargs.autosave,
        pargs.recall,
        pargs.putlogPV,
    )

    edev.publish('VERSION', __version__)
    edev.set_server('Start')

    server = edev.Server(providers=[PVs])
    edev.printi(f'Server for {pargs.prefix} started. Sleeping per cycle: {repr(edev.pvv("sleep"))} S.')
    while True:
        state = edev.serverState()
        if state.startswith('Exit'):
            break
        if not state.startswith('Stop'):
            poll()
        if not edev.sleep():
            periodic_update()

    edev.printi('Server is exited')

