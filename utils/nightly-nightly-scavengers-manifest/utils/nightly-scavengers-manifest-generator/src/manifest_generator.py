import os
import json
import argparse
from typing import List, Dict, Any

def generate_manifest(
    directory: str,
    extensions: List[str] = None,
    output_file: str = None
) -> Dict[str, Any]:
    """
    Scans a directory for files matching specified extensions and generates a manifest.

    Args:
        directory (str): The path to the directory to scan.
        extensions (List[str], optional): A list of file extensions to include (e.g., ['.txt', '.log']).
                                          If None or empty, all files are included.
        output_file (str, optional): Path to a file where the JSON manifest will be saved.
                                     If None, the manifest is returned.

    Returns:
        Dict[str, Any]: A dictionary representing the manifest, or None if output_file is specified.
    """
    manifest = {
        "scan_directory": os.path.abspath(directory),
        "included_extensions": extensions if extensions else ["*"],
        "files": [],
        "summary": {
            "total_files_scanned": 0,
            "total_size_bytes": 0,
            "total_size_human_readable": "0 B"
        }
    }

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if extensions:
                if not any(file.lower().endswith(ext.lower()) for ext in extensions):
                    continue

            try:
                file_size = os.path.getsize(file_path)
                manifest["files"].append({
                    "path": os.path.relpath(file_path, directory),
                    "size_bytes": file_size
                })
                manifest["summary"]["total_files_scanned"] += 1
                manifest["summary"]["total_size_bytes"] += file_size
            except OSError:
                # Handle cases where file might be inaccessible or disappear during scan
                pass

    manifest["summary"]["total_size_human_readable"] = _human_readable_size(manifest["summary"]["total_size_bytes"])

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=4)
        return None
    else:
        return manifest

def _human_readable_size(size_bytes: int) -> str:
    """Converts bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def main():
    parser = argparse.ArgumentParser(
        description="Generate a manifest of files in a directory, optionally filtered by extension."
    )
    parser.add_argument(
        "directory",
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "-e", "--extensions",
        nargs='*',
        help="List of file extensions to include (e.g., .txt .log). If not specified, all files are included."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to an output JSON file. If not specified, the manifest is printed to stdout."
    )

    args = parser.parse_args()

    try:
        manifest = generate_manifest(args.directory, args.extensions, args.output)
        if manifest:
            print(json.dumps(manifest, indent=4))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=os.sys.stderr)
        os.sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.sys.stderr)
        os.sys.exit(1)

if __name__ == "__main__":
    main()
