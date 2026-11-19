# Multibeam Water-Column Vegetation Detection Dataset Workflow

## Overview

This repository provides a Python script and Jupyter Notebook for preparing the
dataset described in “A multibeam water-column dataset with frame-based annotations
for vegetation-like acoustic target detection”. The workflow validates existing JPG
frames and YOLO annotations, organizes copies by survey-line ID and generates summary
metadata. A bundled three-frame example runs without input-path edits.

## Repository contents

- [prepare_dataset.py](prepare_dataset.py): shared preparation functions and command-line workflow.
- [prepare_dataset.ipynb](prepare_dataset.ipynb): sequential notebook using the same functions.
- [wcd_detection_dataset.yml](wcd_detection_dataset.yml): Conda environment using the shared requirements.
- [requirements.txt](requirements.txt): direct Python dependencies for preparation and notebook use.
- [dataset/](dataset/): full-dataset reference metadata and class definition; no full image/label collection.
- [examples/](examples/README.md): three real image/annotation pairs in `input_data/<line_id>/` folders.

## Dataset

The full dataset contains **67,681 frames**, **26,358 annotated frames** and
**188,684 bounding boxes**, with one intended class: `vegetation_like_target`.
Full images and annotations are distributed through
[Figshare](https://doi.org/10.6084/m9.figshare.32196405), separately from this code.
The bundled example demonstrates execution only.

## Annotation format

Each nonempty annotation row uses normalized YOLO coordinates:

```text
0 x_center y_center width height
```

**Class ID 0 = vegetation_like_target.** Width and height must be positive, and
all four coordinate values must be finite and within [0, 1]. Every annotation file
must correspond to an existing JPG with the same basename. An image without
bounding-box annotations may have no label file or an empty label file.

## Quick start

Clone/download the repository and open a terminal in its root:

```bash
git clone https://github.com/neobassist/mbes-water-column-dataset-workflow.git
cd mbes-water-column-dataset-workflow
```

Use Python 3.12 and choose one setup option. Package installation needs internet
access; the bundled example itself uses local input files only.

### Option A: Conda

```bash
conda env create -f wcd_detection_dataset.yml
conda activate wcd_detection_dataset
```

### Option B: pip/venv

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, create the environment with `py -3.12 -m venv .venv` and activate it
with `.venv\Scripts\activate`.

## Run the bundled example

With the chosen environment active:

```bash
python prepare_dataset.py
```

Or register its kernel and open the notebook:

```bash
python -m ipykernel install --sys-prefix --name wcd_detection_dataset --display-name "WCD dataset"
python -m notebook prepare_dataset.ipynb
```

Select **WCD dataset**, then **Restart Kernel and Run All Cells**. Leave the default
configuration unchanged. Open the notebook from the repository directory; its root
finder also accepts a working directory below it. Script defaults are anchored to
the script location, so the script can be invoked from another working directory.

For automated notebook execution from the repository root, after kernel setup:

```bash
python -m nbconvert --to notebook --execute prepare_dataset.ipynb --ExecutePreprocessor.kernel_name=wcd_detection_dataset --ExecutePreprocessor.timeout=120 --output prepare_dataset.executed.ipynb --output-dir example_output
```

## Run with the full dataset

Download and extract the Figshare dataset. Image archives containing line folders
directly (for example `0022/`) should be extracted into `full_dataset/images/`;
extract the archive containing the top-level `labels/` folder into `full_dataset/`:

```text
full_dataset/
  images/<line_id>/*.jpg
  labels/<line_id>/*.txt
  classes.txt
  metadata.csv
```

In the notebook, change only `DATA_ROOT` in the configuration cell to this dataset
directory, for example `DATA_ROOT = Path("../full_dataset")`. The script equivalent is:

```bash
python prepare_dataset.py --data-root ../full_dataset
```

Original per-line input folders are also accepted, with JPG and TXT files together
under `<data_root>/<line_folder>/`. Folder names must start with a four-digit ID,
optionally followed by `_` or `-`. Per-line `classes.txt` is excluded from frame labels.

The default `OUTPUT_ROOT = None` creates a new run directory beneath `example_output/`.
Optionally choose a new, separate output directory in that cell, or use the script's
`--output-root` option. Full preparation copies the input collection and requires
adequate disk space; already organized Figshare files can also be used directly in
your own analysis. Annotation inputs must use class ID 0; unexpected IDs stop execution.

## Expected output

Each successful run creates `example_output/run_<UTC timestamp>/`:

```text
images/<line_id>/*.jpg
labels/<line_id>/*.txt
metadata.csv
classes.txt
```

The bundled example produces **3 frames, 3 annotated frames and 24 bounding boxes**
across 3 IDs, with 8 files in its run directory. Image and annotation bytes are
preserved. Repeated runs create separate directories; existing output targets are
never overwritten. Automated notebook execution also writes the executed notebook
under `example_output/`. Generated outputs are ignored by Git.

## Data integrity checks

Before output creation, the workflow checks YOLO row syntax, normalized coordinate
ranges, allowed class ID 0, matching annotation/image basenames and duplicate
survey-line IDs. Missing inputs and overlapping or existing output directories
raise clear errors. Unexpected class IDs are rejected without automatic correction.
These checks validate file structure and annotation format, not biological identity.

## Dataset splitting guidance

Because temporally adjacent frames can be highly similar or correspond to the same
sonar ping, random image-level splitting may cause information leakage between
training and evaluation subsets. Survey-line-disjoint, temporally blocked, or
spatially separated splits are therefore recommended where appropriate. Check for
remaining overlap; different line IDs alone do not guarantee spatial independence.
No predefined split is generated.

## Important interpretation note

The **41,323 frames without bounding-box annotations** are unlabelled/background
frames; missing annotations do not establish biological absence. Frames originate
from recorded water-column visualization playback and do not have a one-to-one
correspondence with sonar pings. This workflow organizes existing frames and labels;
it does not process raw sonar, deduplicate frames or train a model.

## License

Code: [MIT](LICENSE). Dataset and bundled example data: **CC BY 4.0**, as specified
with the Figshare dataset.

## Citation

Please cite the associated Scientific Data article when available and the dataset:
[A multibeam water-column dataset with frame-based annotations for vegetation-like acoustic target detection](https://doi.org/10.6084/m9.figshare.32196405).

## Contact

SoonYoung Choi, Korea Institute of Ocean Science and Technology (KIOST)  
sychoi@kiost.ac.kr
