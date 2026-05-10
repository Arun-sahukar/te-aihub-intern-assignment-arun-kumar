#!/usr/bin/env python3
"""
Convert Label Studio JSON export to COCO format.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def convert_to_coco(label_studio_path: str, output_path: str, image_width: int = 640, image_height: int = 480) -> None:
    """
    Convert Label Studio JSON export to COCO format.

    Args:
        label_studio_path: Path to Label Studio export JSON
        output_path: Path for output COCO JSON
        image_width: Default image width (used if not in export)
        image_height: Default image height (used if not in export)
    """
    # Load Label Studio export
    with open(label_studio_path, 'r', encoding='utf-8') as f:
        ls_data = json.load(f)

    # COCO format structure
    coco = {
        "info": {
            "description": "BCCD Blood Cell Detection Dataset - Converted from Label Studio",
            "version": "1.0",
            "year": 2026,
            "contributor": "TE Connectivity AI Hub Intern Assignment",
            "date_created": datetime.now().isoformat()
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "RBC", "supercategory": "blood_cell"},
            {"id": 2, "name": "WBC", "supercategory": "blood_cell"},
            {"id": 3, "name": "Platelets", "supercategory": "blood_cell"}
        ]
    }

    # Category name to ID mapping
    category_map = {"RBC": 1, "WBC": 2, "Platelets": 3}

    annotation_id = 1

    for task_idx, task in enumerate(ls_data):
        image_id = task.get("id", task_idx + 1)

        # Get image info
        image_data = task.get("data", {})
        image_url = image_data.get("image", "")
        image_filename = os.path.basename(image_url) if image_url else f"image_{image_id}.jpg"

        # Get original dimensions from annotation if available
        orig_width = image_width
        orig_height = image_height

        # Add image entry
        coco["images"].append({
            "id": image_id,
            "file_name": image_filename,
            "width": orig_width,
            "height": orig_height
        })

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
                category_id = category_map.get(label)

                if not category_id:
                    continue

                # Get dimensions from result
                original_width = result.get("original_width", orig_width)
                original_height = result.get("original_height", orig_height)

                # Convert percentage-based coordinates to pixels
                x_percent = value.get("x", 0)
                y_percent = value.get("y", 0)
                width_percent = value.get("width", 0)
                height_percent = value.get("height", 0)

                x = (x_percent / 100) * original_width
                y = (y_percent / 100) * original_height
                width = (width_percent / 100) * original_width
                height = (height_percent / 100) * original_height

                # COCO annotation
                coco["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "bbox": [x, y, width, height],
                    "area": width * height,
                    "iscrowd": 0
                })

                annotation_id += 1

    # Save COCO format
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coco, f, indent=2)

    print(f"Converted {len(coco['images'])} images with {len(coco['annotations'])} annotations to COCO format")
    print(f"Output saved to: {output_path}")


def main():
    script_dir = Path(__file__).parent.parent

    # Default paths
    default_input = script_dir / "exports" / "label_studio_export.json"
    default_output = script_dir / "exports" / "coco_format" / "annotations.json"

    # Allow command line arguments
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(default_input)
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(default_output)

    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        print("Please export annotations from Label Studio first.")
        sys.exit(1)

    convert_to_coco(input_path, output_path)


if __name__ == "__main__":
    main()
