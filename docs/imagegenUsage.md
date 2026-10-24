# Using epicsdev.imagegen

`epicsdev.imagegen` is a synthetic EPICS image source for testing image pipelines,
PVA/CA clients, and visualization tools. It creates a two-dimensional Gaussian-blob
image, updates it when control PVs change, and can publish row-wise data for
high-throughput checks.

## Start the generator

From the project root:

```bash
python -m epicsdev.imagegen
```

The default instance name is `0`, so the server prefix becomes:

```text
image0:
```

You can choose a different instance or image size with the standard command-line
options:

```bash
python -m epicsdev.imagegen -i 0 -s 512,512
python -m epicsdev.imagegen -i 1 -s 256,256 -t rs
```

The `-t/--throughputTest` option adds extra row and statistics PVs:

- `r` publishes row waveforms like `row0`, `row1`, ...
- `s` publishes stats like `mean0`, `std0`, `peak2peak0`, ...
- `rs` publishes both row data and statistics

## Main PVs

The generator publishes a standard set of control and output PVs under the
selected prefix, for example `image0:`.

Control PVs:

- `image0:nRows`
- `image0:nCols`
- `image0:nBlobsX`
- `image0:nBlobsY`
- `image0:blobMax`
- `image0:blobSigmaX`
- `image0:blobSigmaY`
- `image0:noiseLevel`
- `image0:gridScaleX`
- `image0:oneRowIndex`

Output PVs:

- `image0:image` - the full 2D image
- `image0:oneRow` - a selected row from the image
- `image0:oneRowMean`, `image0:oneRowStd`, `image0:oneRowPeak2Peak`
- `image0:row0`, `image0:row1`, ... if `-t r` is enabled
- `image0:mean0`, `image0:std0`, `image0:peak2peak0`, ... if `-t s` is enabled

## Adjust the image

After startup, write new values to the control PVs to change the generated image:

```bash
pvput image0:nRows 512
pvput image0:nCols 512
pvput image0:blobMax 2000
pvput image0:noiseLevel 25
pvput image0:gridScaleX 1.0
```

The image is recomputed immediately after each change.

## View the image

The simplest monitor command is:

```bash
python -m imagin -b pva -t 100 image0:image
```

This starts the Imagin viewer in PVA mode and displays the generated `image0:image`
waveform.

For row statistics, a compact plot can be started with:

```bash
python -m pvplot -aV:image0: row0 mean0 std0 peak2peak0
```

This plots the first row together with its mean, standard deviation, and
peak-to-peak values.

## Use the companion Pypeto page

The generator also works well with a small pypeto page. The page class exposes a
`PyPage` object that can be instantiated with the active device prefix, for example:

```python
from imgen_pp import PyPage
page = PyPage(instance='image0:')
```

The generated page provides access to the main controls, status PVs, and launch
buttons for the image view and row-stat plot.

## Recommended quick check

A good first test is:

```bash
python -m epicsdev.imagegen -i 0 -t rs
python -m imagin -b pva -t 100 image0:image
python -m pvplot -aV:image0: row0 mean0 std0 peak2peak0
```

This verifies that the server is running, the image is available, and the row
statistics are updating as expected.
