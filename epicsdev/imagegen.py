"""EPICS image generator based on epicsdev.
Generates an image with a grid of noisy Gaussian blobs, with parameters 
defined by PVs. 
The image is recomputed and published when the parameters are changed via PVs. 
Random normal noise is added to the image on each update, without changing 
the underlying blob pattern.
PVs representing image rows and statistics PVs are updated periodically.
"""
# pylint: disable=invalid-name
__version__= 'v0.1.3 26-10-2023'# pylinting, option added: --rotation
import argparse
from dataclasses import dataclass
import numpy as np
from scipy import ndimage

from epicsdev import epicsdev as edev

F = "features"
T = "type"
U = "units"
LL = "limitLow"
LH = "limitHigh"
SET = "setter"
RNG = np.random.default_rng()

#``````````````````Module attributes
ElapsedTime = {'blur': 0., 'publish': 0., 'poll': 0.}

@dataclass(slots=True)
class C_():
    """Class to hold module-level variables."""
    cyclesSinceUpdate = 0
    image = None

def blurred(noise_level, image):
    """Return blurred image with additive noise."""
    if noise_level > 0:
        imageOut = image + RNG.normal(0.0, noise_level, size=image.shape)
    else:
        imageOut = image
    return imageOut.astype(np.int16)

def _gaussian_blob_grid_image() -> np.ndarray:
    """Build image with a regular grid of Gaussian blobs."""
    n_rows = int(edev.pvv("nRows"))
    n_cols = int(edev.pvv("nCols"))
    n_blobs_x = int(edev.pvv("nBlobsX"))
    n_blobs_y = int(edev.pvv("nBlobsY"))
    blob_max = float(edev.pvv("blobMax"))
    sigmax = float(edev.pvv("blobSigmaX"))
    sigmay = float(edev.pvv("blobSigmaY"))

    yy, xx = np.indices((n_rows, n_cols), dtype=np.float32)
    image = np.zeros((n_rows, n_cols), dtype=np.float32)

    dx = n_cols / (n_blobs_x)/2 if n_blobs_x > 0 else n_cols
    dy = n_rows / (n_blobs_y)/2 if n_blobs_y > 0 else n_rows
    if n_blobs_x > 0 and n_blobs_y > 0 and blob_max > 0:
        x_centers = edev.pvv('gridScaleX')\
            * np.linspace(dx, n_cols - dx, n_blobs_x, dtype=np.float32)
        edev.printv(f"Blob centers X before scaling: {x_centers}")
        # Scale centers with respect to the center of the image
        x_centers += n_cols/2. * (1 - edev.pvv('gridScaleX'))

        edev.printv(f"Blob centers X after scaling: {x_centers}")
        y_centers = np.linspace(dy, n_rows - dy, n_blobs_y, dtype=np.float32)
        edev.printv(f"Blob centers X: {x_centers}, Y: {y_centers}")

        for cx in x_centers:
            for cy in y_centers:
                r2 = (xx - cx) ** 2 / (sigmax * sigmax) + (yy - cy) ** 2 / (sigmay * sigmay)
                image += blob_max * np.exp(-r2)
    return image

def rotate(data,degree):
    """Rotate the image by degree, if degree is not a multiple of 90 then use ndimage.rotate"""
    degree += pargs.rotate
    fracp,n = np.modf(degree/90)
    datao = data
    if fracp == 0:
        datao = np.rot90(data,int(n)) # fast rotate by integral of 90 degree
    else:
        #if degree: data = st.rotate(data, degree, resize = True, preserve_range = True)
        if degree:
            datao = ndimage.rotate(data, degree, reshape = True, order=1)
    return datao

def publish_image() -> None:
    """Recompute and publish image from current parameter PVs."""
    C_.image = _gaussian_blob_grid_image()
    if pargs.rotate != 0.0:
        C_.image = rotate(C_.image, pargs.rotate)
    image = blurred(edev.pvv("noiseLevel"), C_.image)

    edev.publish("image", image)

    # for high-throughput case: publish row PVs and statistics PVs if requested
    if 'r' in pargs.throughputTest:
        for row in range(min(pargs.nrows, image.shape[0])):
            edev.publish(f"row{row}", image[row])

def _set_and_regenerate(value, spv):
    """Generic setter that also rebuilds image."""
    edev.publish(spv.name, value)
    publish_image()

def my_pv_defs():
    """Application PV definitions."""
    pvdefs = [
["nRows","Number of rows in the image",pargs.nrows,
            {F: "W", LL: 1, LH: 100000, SET: _set_and_regenerate},],
["nCols","Number of columns in the image",pargs.ncols,
            {F: "W", LL: 10, LH: 1000000, SET: _set_and_regenerate},],
["oneRow","One row of the image, selected by oneRowIndex PV",
            np.zeros(pargs.ncols, dtype="int16"),],
["oneRowIndex","Index of the row to be published in oneRow PV",60,
            {F: "W", LL: 0, LH: pargs.nrows-1, SET: _set_and_regenerate},],
["oneRowMean","Mean of one row of the image",0.0,],
["oneRowStd","Standard deviation of one row of the image",0.0,],
["oneRowPeak2Peak","Peak-to-peak of one row of the image",0.0,],
["nBlobsX","Number of blobs along X axis", 3,
            {F: "W", LL: 0, LH: 100, SET: _set_and_regenerate},],
["nBlobsY","Number of blobs along Y axis", 3,
            {F: "W", LL: 0, LH: 100, SET: _set_and_regenerate},],
["blobMax","Blob maximum", 1000,
            {F: "W", LL: 0, LH: 65535, SET: _set_and_regenerate},],
["blobSigmaX","Blob sigma X", 14.0,
            {F: "W", LL: 0.1, LH: 1000.0, SET: _set_and_regenerate},],
["blobSigmaY","Blob sigma Y", 8.0,
            {F: "W", LL: 0.1, LH: 1000.0, SET: _set_and_regenerate},],
["noiseLevel","Noise level", 100.0,
            {F: "W", LL: 0.0, LH: 1000.0, SET: _set_and_regenerate},],
["gridScaleX","Scale of the horizontal grid of blobs", 1.0,
            {F: "W", SET: _set_and_regenerate},],
["image","Image",np.zeros((pargs.nrows, pargs.ncols), dtype="int16"),],
    ]

    # for high-throughput case: add row PVs and statistics
    for row in range(pargs.nrows):
        if 'r' in pargs.throughputTest:
            pvdefs.append(
[f"row{row}", f"Row {row} of the image",
                    np.zeros(pargs.ncols, dtype="int16")*row])
        if 's' in pargs.throughputTest:
            pvdefs.extend([
[f'mean{row}', f'Mean of rows {row}',0.0],
[f'std{row}', f'Standard deviation of rows {row}', 0.0],
[f'peak2peak{row}', f'Peak-to-peak of rows {row}', 0.0],
                ])
    return pvdefs

def periodic_update():
    """Perform periodic update"""
    edev.printv(f'Elapsed times during last {C_.cyclesSinceUpdate} cycles:'
        f'{[(name, round(v,4)) for name, v in ElapsedTime.items()]}')
    C_.cyclesSinceUpdate = 0
    for key in ElapsedTime:
        ElapsedTime[key] = 0.

def poll():
    """Device polling function, called every cycle when server is running.
    Recompute image and publish row PVs and statistics periodically
    """
    C_.cyclesSinceUpdate += 1
    ts0 = timer()
    image = blurred(edev.pvv("noiseLevel"), C_.image)
    ElapsedTime['blur'] += timer() - ts0

    # publish one row of the image, selected by oneRowIndex PV
    one_row_index = int(edev.pvv("oneRowIndex"))
    if 0 <= one_row_index < image.shape[0]:
        edev.publish("oneRow", image[one_row_index])
        edev.publish("oneRowMean", np.mean(image[one_row_index]))
        edev.publish("oneRowStd", np.std(image[one_row_index]))
        edev.publish("oneRowPeak2Peak", np.ptp(image[one_row_index]))

    if len(pargs.throughputTest) == 0:
        publish_image()
    else: # for high-throughput tests: publish row PVs and statistics PVs if requested
        for row in range(min(pargs.nrows, image.shape[0])):
            ts1 = timer()
            if 'r' in pargs.throughputTest:
                edev.publish(f"row{row}", image[row])
            if 's' in pargs.throughputTest:
                edev.publish(f'mean{row}', np.mean(image[row]))
                edev.publish(f'std{row}', np.std(image[row]))
                edev.publish(f'peak2peak{row}', np.ptp(image[row]))
            ElapsedTime['publish'] += timer() - ts1

    ElapsedTime['poll'] += timer() - ts0

#``````````````````Argument parsing
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog=f'{__version__}'
)
parser.add_argument("-a", "--autosave", nargs="?", default="",help=
    'Autosave control. If not given, then autosave is enabled with default '
    'directory $OPERATIONS/app_store/pvCache when OPERATIONS is defined, '
    'otherwise /operations/app_store/pvCache. '
    'If given without argument, then autosave is disabled. '
    'If a file name is given, then it is used for autosave.')
parser.add_argument("-c", "--recall", action="store_false", help=
    'If given: Do not load initial values from pvCache file. '
    'That is useful when you want to start with default values, '
    'but do not want to disable autosave. By default, the initial '
    'values are loaded from the cache file if it exists.')
parser.add_argument("-t", "--throughputTest", nargs="?", default="", help=
    "Options for high-throughput testing: -gr publishes array PVs, '"
    "-gs publishes statistics PVs, -grs publishes both"                    )
parser.add_argument("-i", "--instance", default="0")
parser.add_argument("-s", "--shape", default="120,120", help=
    "Initial number of rows and columns in the image."  )
parser.add_argument("-p", "--putlogPV", default="putlog:dump")
parser.add_argument("-r", "--rotate", type=float, default=0.0, help=
    "Rotate the image by this angle (degrees) before publishing")
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument('device', nargs='?', default='image', help=
    'Device name, the prefix for all generated PVs <prefix><instance>:')
pargs = parser.parse_args()
pargs.nrows, pargs.ncols = [int(s) for s in pargs.shape.split(',')]
edev.printi(f"Parsed arguments: {pargs}")
if pargs.rotate != 0.0:
    edev.printi(f"Image will be rotated by {pargs.rotate} degrees before publishing")

prefix = f"{pargs.device}{pargs.instance}:"
pvs = edev.init_epicsdev(
    prefix,
    my_pv_defs(),
    pargs.verbose,
    None,
    None,
    pargs.autosave,
    pargs.recall,
    pargs.putlogPV,
)

publish_image()
edev.set_server("Start")

server = edev.Server(providers=[pvs])
edev.printi(f"Server started. Sleeping per cycle: {repr(edev.pvv('sleep'))} S.")

while True:
    state = edev.serverState()
    if state.startswith("Exit"):
        break
    if not state.startswith('Stop'):
        poll()
    if not edev.sleep():# Sleep and update performance metrics periodically
        periodic_update()

edev.printi("Server exited")
