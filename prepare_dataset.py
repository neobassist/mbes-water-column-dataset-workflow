"""Validate and copy YOLO water-column frames without modifying source bytes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import math
import re
import shutil

import pandas as pd
from tqdm.auto import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent
CLASS_NAME = "vegetation_like_target"


def validate_label(path):
    """Reject unexpected class IDs; never harmonize or rewrite annotations."""
    count = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"{path}:{number}: expected five YOLO fields")
        if fields[0] != "0":
            raise ValueError(f"{path}:{number}: unexpected class ID {fields[0]!r}; "
                             "allowed class ID is 0 (vegetation_like_target). "
                             "Use the corrected dataset; no automatic remapping is performed.")
        try:
            x, y, w, h = map(float, fields[1:])
        except ValueError as exc:
            raise ValueError(f"{path}:{number}: non-numeric coordinates") from exc
        if not all(math.isfinite(v) and 0 <= v <= 1 for v in (x, y, w, h)) or w <= 0 or h <= 0:
            raise ValueError(f"{path}:{number}: invalid normalized YOLO coordinates")
        count += 1
    return count


def collect_inputs(data_root):
    """Accept extracted Figshare images/labels or original per-line folders."""
    structured = (data_root / "images").is_dir()
    image_root = data_root / "images" if structured else data_root
    label_root = data_root / "labels" if structured else data_root
    if structured and not label_root.is_dir():
        raise FileNotFoundError("Extract labels.zip alongside images/ before running.")
    groups, seen = [], set()
    for folder in sorted(image_root.iterdir()):
        if not folder.is_dir() or folder.name.startswith((".", "__")):
            continue
        images = sorted(folder.glob("*.jpg"))
        label_folder = label_root / folder.name if structured else folder
        labels = sorted(p for p in label_folder.glob("*.txt") if p.name != "classes.txt")
        if not images and not labels:
            continue
        match = re.match(r"^(\d{4})(?:$|[_-])", folder.name)
        if not match:
            raise ValueError(f"Expected a four-digit survey-line ID: {folder.name}")
        line_id = match.group(1)
        if line_id in seen:
            raise ValueError(f"Duplicate output survey-line ID: {line_id}")
        seen.add(line_id)
        image_stems = {p.stem for p in images}
        boxes = {}
        for label in labels:
            if label.stem not in image_stems:
                raise ValueError(f"Annotation without matching JPG: {label}")
            boxes[label] = validate_label(label)
        groups.append((line_id, images, boxes))
    if structured:
        orphan_lines = [p.name for p in label_root.iterdir()
                        if p.is_dir() and not p.name.startswith((".", "__"))
                        and p.name not in {g.name for g in image_root.iterdir() if g.is_dir()}
                        and any(p.glob("*.txt"))]
        if orphan_lines:
            raise ValueError(f"Label survey lines without image directories: {orphan_lines}")
    if not groups or not any(images for _, images, _ in groups):
        raise ValueError(f"No JPG frames found under {image_root}")
    return groups


def prepare_dataset(data_root=None, output_root=None):
    """Prevalidate all labels, then copy to a new, non-overlapping directory."""
    data_root = Path(data_root).expanduser().resolve() if data_root is not None else PROJECT_ROOT / "examples" / "input_data"
    if not data_root.is_dir():
        raise FileNotFoundError(f"Input directory not found: {data_root}")
    if output_root is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        output_root = PROJECT_ROOT / "example_output" / f"run_{stamp}"
    else:
        output_root = Path(output_root).expanduser().resolve()
    if output_root == data_root or output_root in data_root.parents or data_root in output_root.parents:
        raise ValueError("Input and output directories must not overlap")
    if output_root.exists():
        raise FileExistsError(f"Output already exists; choose a new directory: {output_root}")
    groups = collect_inputs(data_root)  # No output is created if validation fails.
    output_root.mkdir(parents=True, exist_ok=False)
    rows = []
    for line_id, images, boxes in tqdm(groups, desc="Processing survey lines"):
        image_dir = output_root / "images" / line_id
        label_dir = output_root / "labels" / line_id
        image_dir.mkdir(parents=True)
        label_dir.mkdir(parents=True)
        for image in images:
            shutil.copy2(image, image_dir / image.name)
        for label in boxes:
            shutil.copy2(label, label_dir / label.name)
        rows.append(dict(line_id=line_id, total_frames=len(images),
                         annotated_frames=sum(n > 0 for n in boxes.values()),
                         total_bboxes=sum(boxes.values())))
    (output_root / "classes.txt").write_text(CLASS_NAME + "\n", encoding="utf-8")
    df = pd.DataFrame(rows).sort_values("line_id")
    df.to_csv(output_root / "metadata.csv", index=False)
    print(f"Output directory: {output_root}")
    print(f"Total survey lines: {len(df)}")
    for column in ("total_frames", "annotated_frames", "total_bboxes"):
        print(f"{column}: {df[column].sum()}")
    return df, output_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, help="Extracted dataset or original per-line input directory")
    parser.add_argument("--output-root", type=Path, help="New directory; existing directories are never overwritten")
    args = parser.parse_args()
    prepare_dataset(args.data_root, args.output_root)


if __name__ == "__main__":
    main()
