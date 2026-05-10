#!/usr/bin/env python3
"""
Convert Label Studio JSON export to YOLO format.
"""

import json
import os
import sys
from pathlib import Path


def convert_to_yolo(label_studio_path: str, output_dir: str) -> None:
    """
    Convert Label Studio JSON export to YOLO format.

    Args:
        label_studio_path: Path to Label Studio export JSON
        output_dir: Directory for output YOLO txt files
    """
    # Load Label Studio export
    with open(label_studio_path, 'r', encoding='utf-8') as f:
        ls_data = json.load(f)

    # Category name to ID mapping (0-indexed for YOLO)
    category_map = {"RBC": 0, "WBC": 1, "Platelets": 2}

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create classes.txt
    classes_path = os.path.join(output_dir, "classes.txt")
    with open(classes_path, 'w') as f:
        f.write("RBC\nWBC\nPlatelets\n")

    converted_count = 0
    annotation_count = 0

    for task in ls_data:
        # Get image filename
        image_data = task.get("data", {})
        image_url = image_data.get("image", "")
        image_filename = os.path.basename(image_url) if image_url else f"image_{task.get('id', 0)}.jpg"

        # Output txt filename (same name as image, different extension)
        txt_filename = os.path.splitext(image_filename)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)

        yolo_lines = []

        # Process annotations
        annotations = task.get("annotations", [])
        for annotation in annotations:
            results = annotation.get("result", [])

            for result in results:
                if result.get("type") != "rectanglelabels":
                    continue

                value = result.get("value", {})
                labels = value.get("rectanglelabels", [])

                if not labels:
                    continue

                label = labels[0]
                class_id = category_map.get(label)

                if class_id is None:
                    continue

                # Get percentage-based coordinates from Label Studio
                x_percent = value.get("x", 0)
                y_percent = value.get("y", 0)
                width_percent = value.get("width", 0)
                height_percent = value.get("height", 0)

                # Convert to YOLO format (center x, center y, width, height - all normalized 0-1)
                x_center = (x_percent + width_percent / 2) / 100
                y_center = (y_percent + height_percent / 2) / 100
                width_norm = width_percent / 100
                height_norm = height_percent / 100

                # YOLO format: class_id x_center y_center width height
                yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}")
                annotation_count += 1

        # Write YOLO annotation file
        with open(txt_path, 'w') as f:
            f.write("\n".join(yolo_lines))

        converted_count += 1

    print(f"Converted {converted_count} images with {annotation_count} annotations to YOLO format")
    print(f"Output saved to: {output_dir}")
    print(f"Classes file: {classes_path}")


def main():
    script_dir = Path(__file__).parent.parent

    # Default paths
    default_input = script_dir / "exports" / "label_studio_export.json"
    default_output = script_dir / "exports" / "yolo_format"

    # Allow command line arguments
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(default_input)
    output_dir = sys.argv[2] if len(sys.argv) > 2 else str(default_output)

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        print("Please export annotations from Label Studio first.")
        sys.exit(1)

    convert_to_yolo(input_path, output_dir)


if __name__ == "__main__":
    main()
