# Using epicsdev.imagegen

`epicsdev.imagegen` is a synthetic EPICS image source for testing image pipelines,
PVA/CA clients, and visualization tools. It creates a two-dimensional Gaussian-blob
image, updates it when control PVs change, and can publish row-wise data for
high-throughput checks.

## Start the generator

From the project root:

```bash
python -m epicsdev.imagegen -r30
```

The default instance name is `0`, so the server prefix becomes:

```text
image:0:
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
selected prefix, for example `image:0:`.

Control PVs:

- `image:0:nRows`
- `image:0:nCols`
- `image:0:nBlobsX`
- `image:0:nBlobsY`
- `image:0:blobMax`
- `image:0:blobSigmaX`
- `image:0:blobSigmaY`
- `image:0:noiseLevel`
- `image:0:gridScaleX`
- `image:0:oneRowIndex`

Output PVs:

- `image:0:image` - the full 2D image
- `image:0:oneRow` - a selected row from the image
- `image:0:oneRowMean`, `image:0:oneRowStd`, `image:0:oneRowPeak2Peak`
- `image:0:row0`, `image:0:row1`, ... if `-t r` is enabled
- `image:0:mean0`, `image:0:std0`, `image:0:peak2peak0`, ... if `-t s` is enabled

## Adjust the image

After startup, write new values to the control PVs to change the generated image:

```bash
pvput image:0:nRows 512
pvput image:0:nCols 512
pvput image:0:blobMax 2000
pvput image:0:noiseLevel 25
pvput image:0:gridScaleX 1.0
```

The image is recomputed immediately after each change.

## View the image

The simplest monitor command is:

```bash
python -m imagin -b pva -t 100 image:0:image
```

This starts the Imagin viewer in PVA mode and displays the generated `image:0:image`
waveform.

For row statistics, a compact plot can be started with:

```bash
python -m pvplot -aV:image:0:oneRow 'Mean Std Peak2Peak'
```

This plots mean, standard deviation and peak-to-peak values of row, indexed by oneRowIndex PV.

## Use the companion Pypeto page

The generator also works well with a small pypeto page. The page class exposes a
`PyPage` object that can be instantiated with the active device prefix, for example:

```python
from imagegen_pp import PyPage
page = PyPage(instance='image:0:')
```

The generated page provides access to the main controls, status PVs, and launch
buttons for the image view and row-stat plot.

## Recommended quick check

A good first test is:

```bash
python -m epicsdev.imagegen -i 0 -t rs -r30
python -m imagin -b pva -t 100 image:0:image
python -m pvplot -aV:image:0:oneRow 'Mean Std Peak2Peak'
```

This verifies that the server is running, the image is available, and the row
statistics are updating as expected.
