import os
import json
import argparse
from datetime import datetime

def _scan_directory(path):
    """Scans a directory and returns a dictionary of file metadata."""
    baseline_data = {}
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                stat = os.stat(file_path)
                baseline_data[file_path] = {
                    "size": stat.st_size,
                    "mtime": stat.st_mtime, # Modification time as float timestamp
                    "ctime": stat.st_ctime, # Creation time as float timestamp
                }
            except FileNotFoundError:
                # Should not happen during os.walk, but good practice
                pass
    return baseline_data

def generate_baseline(target_path, output_file):
    """Generates a baseline of file metadata for a given path."""
    if not os.path.isdir(target_path):
        print(f"Error: Target path '{target_path}' is not a directory.")
        return False

    print(f"Generating baseline for '{target_path}'...")
    baseline_data = _scan_directory(target_path)

    try:
        with open(output_file, 'w') as f:
            json.dump(baseline_data, f, indent=2)
        print(f"Baseline saved to '{output_file}'.")
        return True
    except IOError as e:
        print(f"Error saving baseline to '{output_file}': {e}")
        return False

def check_anomalies(target_path, baseline_file):
    """Compares current file system state against a baseline and reports anomalies."""
    if not os.path.isdir(target_path):
        print(f"Error: Target path '{target_path}' is not a directory.")
        return False

    if not os.path.exists(baseline_file):
        print(f"Error: Baseline file '{baseline_file}' not found. Generate one first.")
        return False

    try:
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading baseline from '{baseline_file}': {e}")
        return False

    print(f"Checking for anomalies in '{target_path}' against '{baseline_file}'...")
    current_data = _scan_directory(target_path)

    anomalies_found = False
    print("\n--- Anomalies Report ---")

    # Check for removed files
    for path in baseline_data:
        if path not in current_data:
            print(f"  [REMOVED] {path}")
            anomalies_found = True

    # Check for added or modified files
    for path, current_meta in current_data.items():
        if path not in baseline_data:
            print(f"  [ADDED] {path}")
            anomalies_found = True
        else:
            baseline_meta = baseline_data[path]
            # Compare size and mtime. ctime can change on copy, so mtime is better for content changes.
            if current_meta["size"] != baseline_meta["size"] or \
               current_meta["mtime"] != baseline_meta["mtime"]:
                print(f"  [MODIFIED] {path}")
                print(f"    Baseline: Size={baseline_meta['size']}, MTime={datetime.fromtimestamp(baseline_meta['mtime']).strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Current:  Size={current_meta['size']}, MTime={datetime.fromtimestamp(current_meta['mtime']).strftime('%Y-%m-%d %H:%M:%S')}")
                anomalies_found = True

    if not anomalies_found:
        print("  No temporal anomalies detected. All clear!")
    print("------------------------")
    return anomalies_found

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Anomaly Tracker: Detects unexpected file system changes."
    )
    parser.add_argument(
        "action",
        choices=["baseline", "check"],
        help="Action to perform: 'baseline' to generate a new baseline, 'check' to compare against an existing one."
    )
    parser.add_argument(
        "path",
        help="The target directory path to scan or check."
    )
    parser.add_argument(
        "--output",
        "-o",
        default="anomaly_baseline.json",
        help="Output file for baseline generation or input file for anomaly checking."
    )

    args = parser.parse_args()

    if args.action == "baseline":
        generate_baseline(args.path, args.output)
    elif args.action == "check":
        check_anomalies(args.path, args.output)

if __name__ == "__main__":
    main()
