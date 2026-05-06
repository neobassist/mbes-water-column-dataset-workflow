# Multibeam Water-Column Vegetation Detection Dataset Workflow

This repository provides the code and environment configuration used to construct the multibeam water-column dataset described in the associated Scientific Data article.

The workflow converts annotated water-column image frames into a standardized dataset structure suitable for machine-learning applications, particularly object detection of vegetation-like acoustic targets.

---

## Included files

- `prepare_dataset.py`  
  Python script for dataset restructuring, organization, and metadata generation.

- `prepare_dataset.ipynb`  
  Jupyter Notebook version of the dataset preparation workflow.

- `wcd_detection_dataset.yml`  
  Conda environment file for reproducing the Python environment.

- `metadata.csv`  
  Per-line dataset statistics (number of frames, annotated frames, bounding boxes).

- `classes.txt`  
  Single-class definition file (`vegetation_like_target`).

---

## Portability notes

- The workflow uses **relative paths** (no machine-specific absolute paths such as `/Users/...`).
- Input and output directories are defined at the top of the script using relative paths (e.g., `./input_data`, `./dataset`).
- The workflow can be executed after cloning/downloading the repository, provided the expected input folder structure is prepared.
- All code comments are written in English.

---

## Expected input / output folders

### Input structure

The workflow expects raw annotated data to be placed in:

```
input_data/
├── 0000-2022_albinism_WCD-1_300kHz/
├── 0002_2022_albinism_WCD-1_300kHz/
├── ...
```

Each survey line folder contains:

- `.jpg` image frames extracted from water-column video playback
- `.txt` annotation files in YOLO format (only for annotated frames)
- `classes.txt` (generated during annotation)

Note: Annotation files are only present for frames containing detectable targets.

---

### Output structure

The processed dataset is generated as:

```
dataset/
├── images/
│   ├── 0000/
│   ├── 0002/
│   ├── ...
│
├── labels/
│   ├── 0000/
│   ├── 0002/
│   ├── ...
│
├── metadata.csv
├── classes.txt
```

- `images/`: Frame images organized by survey line  
- `labels/`: Corresponding YOLO annotation files  
- `metadata.csv`: Dataset statistics per survey line  
- `classes.txt`: Unified class definition  

---

## How to run

1. Create the conda environment:

```bash
conda env create -f wcd_detection_dataset.yml
conda activate wcd_detection_dataset
```

2. Run the dataset preparation script:

```bash
python prepare_dataset.py
```

3. (Optional) Run the Jupyter Notebook:

```bash
jupyter notebook prepare_dataset.ipynb
```

---

## Dataset characteristics

- Total survey lines: 24  
- Total frames: 67,681  
- Annotated frames: 26,358  
- Total bounding boxes: 188,684  

All annotated objects are assigned to a single class:

```
vegetation_like_target
```

---

## Annotation format

Annotations follow the YOLO object detection format:

```
[class_id] [x_center] [y_center] [width] [height]
```

- All objects use `class_id = 0`
- Each line represents one detected object

---

## Notes

- No predefined training, validation, or test split is included  
- Frames are derived from video playback and represent temporally continuous sampling  
- Frames do not correspond exactly to individual sonar pings  
- The dataset is designed for **object detection**, not classification  

---

## Data integrity

Basic integrity checks are performed during dataset preparation:

- Verification of image copy completeness  
- Consistency between source and processed frame counts  
- Validation of annotation files and bounding box counts  
- One-to-one correspondence between image and label files  

---

## License

The code provided in this repository is released under the MIT License.

The associated dataset is distributed separately via Figshare under the CC BY 4.0 license.

---

## Citation

Please cite the associated Scientific Data article (and dataset DOI) once the manuscript is published.

---

## Contact

SoonYoung Choi  
Dokdo Research Center, Korea Institute of Ocean Science and Technology (KIOST)
sychoi@kiost.ac.kr