import os
import json
from datetime import datetime

def generate_manifest(directory_path: str) -> dict:
    """
    Generates a summary manifest of files in the given directory.

    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        dict: A dictionary containing the manifest details.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    manifest = {
        "directory": os.path.abspath(directory_path),
        "summary": {
            "total_files": 0,
            "total_directories": 0,
            "total_size_bytes": 0,
            "unique_extensions": set() # Use set for uniqueness, convert to list later
        },
        "file_type_breakdown": {}
    }

    for root, dirs, files in os.walk(directory_path):
        manifest["summary"]["total_directories"] += len(dirs)
        for filename in files:
            manifest["summary"]["total_files"] += 1
            file_path = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(file_path)
                file_mtime = os.path.getmtime(file_path)
            except OSError: # File might be inaccessible or disappear during walk
                # Skip this file if it's inaccessible or disappears
                continue

            manifest["summary"]["total_size_bytes"] += file_size

            _, ext = os.path.splitext(filename)
            ext = ext.lower() if ext else "no_extension"
            manifest["summary"]["unique_extensions"].add(ext)

            if ext not in manifest["file_type_breakdown"]:
                manifest["file_type_breakdown"][ext] = {
                    "count": 0,
                    "total_size_bytes": 0,
                    "latest_modified": None # Will store ISO 8601 string
                }

            manifest["file_type_breakdown"][ext]["count"] += 1
            manifest["file_type_breakdown"][ext]["total_size_bytes"] += file_size

            current_mtime_dt = datetime.fromtimestamp(file_mtime)
            # Format as ISO 8601 with 'Z' for UTC, seconds precision
            current_mtime_iso = current_mtime_dt.isoformat(timespec='seconds') + 'Z'

            # Update latest_modified if current file is newer
            if manifest["file_type_breakdown"][ext]["latest_modified"] is None or \
               current_mtime_iso > manifest["file_type_breakdown"][ext]["latest_modified"]:
                manifest["file_type_breakdown"][ext]["latest_modified"] = current_mtime_iso

    manifest["summary"]["unique_extensions"] = sorted(list(manifest["summary"]["unique_extensions"]))
    return manifest

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python src/manifest_generator.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    try:
        result = generate_manifest(target_directory)
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
