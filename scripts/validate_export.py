#!/usr/bin/env python3
"""
Validation script for Label Studio export file.
Checks if the export file exists and contains valid annotations.
"""

import json
import os
import sys
from pathlib import Path


def validate_label_studio_export(export_path: str) -> dict:
    """
    Validate a Label Studio JSON export file.

    Args:
        export_path: Path to the Label Studio export JSON file

    Returns:
        Dictionary with validation results
    """
    results = {
        "file_exists": False,
        "valid_json": False,
        "total_tasks": 0,
        "annotated_tasks": 0,
        "total_annotations": 0,
        "labels_found": set(),
        "errors": []
    }

    # Check if file exists
    if not os.path.exists(export_path):
        results["errors"].append(f"File not found: {export_path}")
        return results

    results["file_exists"] = True

    # Try to parse JSON
    try:
        with open(export_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results["errors"].append(f"Invalid JSON: {e}")
        return results
    except Exception as e:
        results["errors"].append(f"Error reading file: {e}")
        return results

    results["valid_json"] = True

    # Validate structure
    if not isinstance(data, list):
        results["errors"].append("Export should be a list of tasks")
        return results

    results["total_tasks"] = len(data)

    # Analyze annotations
    for task in data:
        if not isinstance(task, dict):
            continue

        annotations = task.get("annotations", [])
        if annotations:
            results["annotated_tasks"] += 1

            for annotation in annotations:
                if not isinstance(annotation, dict):
                    continue

                annotation_results = annotation.get("result", [])
                results["total_annotations"] += len(annotation_results)

                for result in annotation_results:
                    if isinstance(result, dict):
                        value = result.get("value", {})
                        if isinstance(value, dict):
                            labels = value.get("rectanglelabels", [])
                            for label in labels:
                                results["labels_found"].add(label)

    # Convert set to list for JSON serialization
    results["labels_found"] = list(results["labels_found"])

    return results


def print_report(results: dict) -> None:
    """Print a formatted validation report."""
    print("\n" + "=" * 50)
    print("LABEL STUDIO EXPORT VALIDATION REPORT")
    print("=" * 50)

    print(f"\nFile exists: {'Yes' if results['file_exists'] else 'No'}")
    print(f"Valid JSON: {'Yes' if results['valid_json'] else 'No'}")

    if results["valid_json"]:
        print(f"\nTotal tasks (images): {results['total_tasks']}")
        print(f"Annotated tasks: {results['annotated_tasks']}")
        print(f"Total bounding boxes: {results['total_annotations']}")
        print(f"Labels found: {', '.join(results['labels_found']) if results['labels_found'] else 'None'}")

    if results["errors"]:
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  - {error}")

    # Summary
    print("\n" + "-" * 50)
    if results["annotated_tasks"] >= 5:
        print("PASS: Minimum 5 annotated images requirement met!")
    else:
        print(f"WARNING: Only {results['annotated_tasks']} images annotated. Minimum required: 5")

    expected_labels = {"RBC", "WBC", "Platelets"}
    found_labels = set(results["labels_found"])
    if expected_labels == found_labels:
        print("PASS: All expected labels (RBC, WBC, Platelets) found!")
    else:
        missing = expected_labels - found_labels
        extra = found_labels - expected_labels
        if missing:
            print(f"WARNING: Missing labels: {missing}")
        if extra:
            print(f"INFO: Additional labels found: {extra}")

    print("=" * 50 + "\n")


def main():
    # Default export path
    script_dir = Path(__file__).parent.parent
    default_export_path = script_dir / "exports" / "label_studio_export.json"

    # Allow command line argument for export path
    if len(sys.argv) > 1:
        export_path = sys.argv[1]
    else:
        export_path = str(default_export_path)

    print(f"Validating export file: {export_path}")

    results = validate_label_studio_export(export_path)
    print_report(results)

    # Exit with error code if validation failed
    if results["errors"] or results["annotated_tasks"] < 5:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
