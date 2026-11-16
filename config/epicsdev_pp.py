"""AI-generated Pypeto control page for the epicsDev:0 live EPICS IOC.
This page exposes the PVs requested by the user as a live control panel in the
pypeto GUI. The file is intended to be loaded by the pypeto application as a
configuration module, e.g. via `python -m pypeto -c config -f ai_epicsdev_pp`.
"""
# pylint: disable=invalid-name
__version__ = 'v0.1.0 2026-11-14'

_ = ''


def span(x, y=1):
    return {'span': [x, y]}


def color(*v):
    return {'color': v[0]} if len(v) == 1 else {'color': list(v)}


def font(size):
    return {'font': ['Arial', size]}


def just(i):
    return {'justify': {0: 'left', 1: 'center', 2: 'right'}[i]}


#LargeFont = {'color': 'light gray', **font(18), 'fgColor': 'dark green'}
ButtonFont = {'font': ['Open Sans Extrabold', 14]}
#HeaderColor = {**color('lightCyan'), **just(1)}
lColor = color('lightGreen')
PyPath = 'python -m'

PREFIX = 'epicsDev:0:'


class PyPage():
    def __init__(self, instance=PREFIX, title='epicsDev:0'):
        """Create the pypeto control page for an epicsDev IOC."""
        self.namespace = 'PVA'
        self.title = title
        self.page = {**color(240, 240, 240)}
        self.columns = {
            1: {'width': 130, 'justify': 'right'},
            2: {'width': 110},
            3: {'width': 130, 'justify': 'right'},
            4: {'width': 110},
            5: {'width': 130, 'justify': 'right'},
            6: {'width': 110},
            7: {'width': 110},
            8: {'width': 110},
            9: {'width': 110},
        }

        D = instance

        PaneP2P = 'c01Mean c01Peak2Peak'
        PaneWF = 'c01Waveform'
        Plot = {
            'Plot': {
                'launch': f'{PyPath} pvplot Y-5:5 -aV:{D} -#0"{PaneP2P}" -#1"{PaneWF}"',
                **lColor,
                **ButtonFont,
            }
        }

        self.rows = [
            ['Device:', D, 'Server:', D + 'server', 'Version:', D + 'VERSION'],
            ['Host:', D + 'HOSTNAME', 'StartTOD:', D + 'STARTTOD', 'Uptime:', D + 'UPTIME'],
            ['CPU load:', D + 'CPU_LOAD', 'Heartbeat:', D + 'HEARTBEAT', 'Alarm:', D + 'alarm'],
            ['Status:', {D + 'status': span(3, 1)}, 'Verbose:', D + 'verbose', 'Cycle:', D + 'cycle'],
            ['Sleep:', D + 'sleep', 'Cycle time:', D + 'cycleTime', 'Throughput:', D + 'throughput'],
            ['Record length:', D + 'recordLength', 'Noise:', D + 'noiseLevel', 'V/div:', D + 'c01VoltsPerDiv'],
            # [{**HeaderColor}, 'Signal', 'PV', 'Signal', 'PV', 'Signal', 'PV', 'Signal', 'PV'],
            ['Mean:', D + 'c01Mean', 'Offset:', D + 'c01Offset', 'P2P:', D + 'c01Peak2Peak'],
            ['Waveform:', {D + 'c01Waveform': span(5, 1)}, 'Time axis:', D + 'tAxis'],
            ['Waveform array:', D + 'waveform', 'Image data:', D + 'image', Plot],
            #['Live data:', {D + 'status': span(2, 1)}, 'Host:', D + 'HOSTNAME', 'Alarm:', D + 'alarm'],
        ]


if __name__ == '__main__':
    page = PyPage()
    print(page.title)
    print(len(page.rows))
