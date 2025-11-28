import os
import json
import argparse
from datetime import datetime

def get_file_metadata(filepath, base_path):
    """
    Collects metadata for a single file.
    """
    try:
        stat_info = os.stat(filepath)
        return {
            "name": os.path.relpath(filepath, base_path),
            "path": filepath,
            "size_bytes": stat_info.st_size,
            "last_modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat() + "Z"
        }
    except OSError:
        return None

def generate_manifest(scan_path):
    """
    Scans the given path and generates a manifest of all files.
    """
    if not os.path.isdir(scan_path):
        raise ValueError(f"Scan path '{scan_path}' is not a valid directory.")

    files_data = []
    total_files = 0
    total_size_bytes = 0

    for root, _, files in os.walk(scan_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            metadata = get_file_metadata(filepath, scan_path)
            if metadata:
                files_data.append(metadata)
                total_files += 1
                total_size_bytes += metadata["size_bytes"]

    return {
        "scan_path": os.path.abspath(scan_path),
        "scan_timestamp": datetime.utcnow().isoformat() + "Z",
        "total_files": total_files,
        "total_size_bytes": total_size_bytes,
        "files": files_data
    }

def main():
    parser = argparse.ArgumentParser(
        description="Generate a manifest of files in a specified directory."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The directory path to scan for resources."
    )
    args = parser.parse_args()

    try:
        manifest = generate_manifest(args.path)
        print(json.dumps(manifest, indent=2))
    except ValueError as e:
        print(f"Error: {e}", file=os.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.stderr)
        exit(1)

if __name__ == "__main__":
    main()
