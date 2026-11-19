# Bundled example

This small subset of the real dataset demonstrates workflow execution only. It
contains three water-column image frames (IDs 0022, 0031 and 0041) and their matching
YOLO annotation files: 3 frames, 3 labels and 24 bounding boxes, all class ID 0
(`vegetation_like_target`). Each `input_data/<line_id>/` folder contains one JPG/TXT pair.

The images are the repository's original three examples; their corresponding
annotations were taken from the associated dataset. Image and annotation contents
are preserved without changing file bytes, bounding-box coordinates or class labels.

This example does not replace the full Scientific Data dataset, which is provided
through [Figshare](https://doi.org/10.6084/m9.figshare.32196405). The example data are
licensed under CC BY 4.0. Cite the associated article and dataset when using them.
See the [main README](../README.md) for setup, execution and expected output.
