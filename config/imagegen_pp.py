"""AI-generated Pypeto page for the epicdev image generator."""
# pylint: disable=invalid-name
# format: pypeto 1.2+

__version__ = 'v0.0.1 2026-11-15'# Version changed
print(f'imagegen {__version__}')

_ = ''
PREFIX = 'image:0:'


def span(x, y=1):
    return {'span': [x, y]}


def color(*v):
    return {'color': v[0]} if len(v) == 1 else {'color': list(v)}


def font(size):
    return {'font': ['Arial', size]}


def just(i):
    return {'justify': {0: 'left', 1: 'center', 2: 'right'}[i]}


def slider(minValue, maxValue):
    """Definition of the GUI element: horizontal slider with flexible range."""
    return {'widget': 'hslider', 'opLimits': [minValue, maxValue], 'span': [2, 1]}


LargeFont = {'color': 'light gray', **font(18), 'fgColor': 'dark green'}
ButtonFont = {'font': ['Open Sans Extrabold', 14]}
LYRow = {'ATTRIBUTES': {'color': 'light yellow'}}
lColor = color('lightGreen')
PyPath = 'python -m'


class PyPage():
    def __init__(self, instance=PREFIX, title='Image generator'):
        """Create the pypeto page for the image generator IOC."""
        self.namespace = 'PVA'
        self.title = title
        self.page = {**color(240, 240, 240)}

        self.columns = {
            1: {'width': 120, 'justify': 'right'},
            2: {'width': 90},
            3: {'width': 120, 'justify': 'right'},
            4: {'width': 90},
            5: {'width': 120, 'justify': 'right'},
            6: {'width': 90},
            7: {'width': 90},
            8: {'width': 90},
            9: {'width': 90},
        }

        D = instance

        ViewImage = {'Image view': {'launch': f'{PyPath} imagin -b pva -t 100 {D}image', **lColor, **ButtonFont}}
        RowPlot = {'Row plot': {'launch': f'{PyPath} pvplot -aV:{D} row0 mean0 std0 peak2peak0', **lColor, **ButtonFont}}
        print(f'pvplot command: {RowPlot}')

        self.rows = [
            ['Device:', D, 'Server:', D + 'server', 'Version:', D + 'VERSION'],
            ['Host:', D + 'HOSTNAME', 'StartTOD:', D + 'STARTTOD', 'Uptime:', D + 'UPTIME'],
            ['CPU load:', D + 'CPU_LOAD', 'Heartbeat:', D + 'HEARTBEAT', 'CA conn.:', D + 'CA_CONN_COUNT'],
            ['Status:', {D + 'status': span(3, 1)}, 'Cycle:', D + 'cycle', 'Verbose:', D + 'verbose'],
            ['Sleep:', D + 'sleep', 'Cycle time:', D + 'cycleTime', 'View:', ViewImage],
            ['Rows:', D + 'nRows', 'Cols:', D + 'nCols', 'Selected row:', D + 'oneRowIndex', 'One row:', D + 'oneRow'],
            ['Blobs X:', D + 'nBlobsX', 'Blobs Y:', D + 'nBlobsY', 'Blob max:', D + 'blobMax', 'Grid X:', D + 'gridScaleX'],
            ['Sigma X:', D + 'blobSigmaX', 'Sigma Y:', D + 'blobSigmaY', 'Noise:', D + 'noiseLevel'],
            ['One-row mean:', D + 'oneRowMean', 'Std:', D + 'oneRowStd', 'Peak2Peak:', D + 'oneRowPeak2Peak', RowPlot],
            ['Image:', {D + 'image': span(6, 1)}],
        ]


if __name__ == '__main__':
    page = PyPage()
    print(page.title)
    print(len(page.rows))
