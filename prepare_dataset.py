# %% [markdown]
"""
# Dataset Preparation for Water-Column Detection

This script restructures raw annotated water-column image data into a standardized
dataset format suitable for publication and machine learning applications.

## Main functions
1. Organize images and annotation files into separate directories
2. Preserve survey line structure
3. Generate metadata statistics
4. Export metadata as CSV file

Dataset preparation workflow for multibeam water-column imagery.
"""

# %%
# Import required libraries for file handling and data processing
import os
import shutil
import pandas as pd
from tqdm import tqdm

# %% [markdown]
"""
## User Configuration

Define input (raw annotated data) and output (final dataset) directories.
"""

# %%
# Path to raw annotated data (user-defined)
# Users should place the input data in the 'input_data/' directory located in the project root.
SOURCE_DIR = "./input_data"

# Path to output dataset (user-defined)
# The processed dataset will be automatically generated in the 'dataset/' directory.
TARGET_DIR = "./dataset"

# Define subdirectories for images and labels
IMAGES_DIR = os.path.join(TARGET_DIR, "images")
LABELS_DIR = os.path.join(TARGET_DIR, "labels")

# %% [markdown]
"""
## Pre-checks

Verify that the input directory exists and warn if the output directory already exists.
"""

# %%
# Check if input directory exists
if not os.path.exists(SOURCE_DIR):
    raise FileNotFoundError(f"Input directory not found: {SOURCE_DIR}")

# Warn if output directory already exists
if os.path.exists(TARGET_DIR):
    print("Warning: TARGET_DIR already exists and may be overwritten.")

# %% [markdown]
"""
## Initialize Output Structure

Create required directories and prepare metadata storage.
"""

# %%
# Create output directories if they do not exist
os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LABELS_DIR, exist_ok=True)

# Initialize list to store metadata for each survey line
metadata = []

# Create a unified classes.txt file with a single class definition
with open(os.path.join(TARGET_DIR, "classes.txt"), "w") as f:
    f.write("vegetation_like_target\n")

# %% [markdown]
"""
## Dataset Restructuring

Process each survey line folder:
- Copy image files to the images directory
- Copy annotation files to the labels directory
- Count total frames, annotated frames, and bounding boxes
- Perform validation checks
"""

# %%
# Iterate over all survey line folders
for line_folder in tqdm(sorted(os.listdir(SOURCE_DIR)), desc="Processing survey lines"):

    src_path = os.path.join(SOURCE_DIR, line_folder)

    if not os.path.isdir(src_path):
        continue

    # Extract line ID
    line_id = line_folder.split("_")[0].replace("-", "")

    # Define output paths
    img_target_path = os.path.join(IMAGES_DIR, line_id)
    lbl_target_path = os.path.join(LABELS_DIR, line_id)

    os.makedirs(img_target_path, exist_ok=True)
    os.makedirs(lbl_target_path, exist_ok=True)

    # Initialize counters
    image_count = 0
    annotated_count = 0
    bbox_count = 0

    # Count original images (for validation)
    original_images = len([f for f in os.listdir(src_path) if f.endswith(".jpg")])

    # Process files
    for file in os.listdir(src_path):

        src_file = os.path.join(src_path, file)

        # Copy images
        if file.endswith(".jpg"):
            shutil.copy2(src_file, os.path.join(img_target_path, file))
            image_count += 1

        # Copy annotation files (exclude classes.txt)
        elif file.endswith(".txt") and file != "classes.txt":
            shutil.copy2(src_file, os.path.join(lbl_target_path, file))
            annotated_count += 1

            with open(src_file, "r") as f:
                bbox_count += len(f.readlines())

    # =========================
    # Validation checks
    # =========================

    # 1. Image count consistency
    if original_images != image_count:
        print(f"Warning: Image count mismatch in line {line_id} "
              f"(original: {original_images}, copied: {image_count})")

    # 2. Annotation vs image sanity
    if annotated_count > image_count:
        print(f"Warning: More annotated frames than images in line {line_id}")

    # 3. Bounding box existence
    if annotated_count > 0 and bbox_count == 0:
        print(f"Warning: Annotated frames exist but no bounding boxes found in line {line_id}")

    # Save metadata
    metadata.append({
        "line_id": line_id,
        "total_frames": image_count,
        "annotated_frames": annotated_count,
        "total_bboxes": bbox_count
    })

# %% [markdown]
"""
## Export Metadata

Convert collected metadata into a DataFrame and save as CSV.
"""

# %%
df = pd.DataFrame(metadata)
df = df.sort_values(by="line_id")

output_csv = os.path.join(TARGET_DIR, "metadata.csv")
df.to_csv(output_csv, index=False)

df.head()

# %% [markdown]
"""
## Summary

Display overall dataset statistics for verification.
"""

# %%
print("\nDataset restructuring completed.\n")

print(f"Output directory: {TARGET_DIR}")
print(f"Metadata file: {output_csv}")

print("\nSummary statistics:")
print(f"Total survey lines: {len(df)}")
print(f"Total frames: {df['total_frames'].sum()}")
print(f"Annotated frames: {df['annotated_frames'].sum()}")
print(f"Total bounding boxes: {df['total_bboxes'].sum()}")