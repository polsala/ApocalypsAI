import os
import argparse
import json
from datetime import datetime, timezone

def generate_manifest(scan_path: str) -> dict:
    """
    Scans a directory and generates a manifest of file types, counts, and sizes.

    Args:
        scan_path: The path to the directory to scan.

    Returns:
        A dictionary containing the manifest data.
    """
    if not os.path.isdir(scan_path):
        raise ValueError(f"Path '{scan_path}' is not a valid directory.")

    manifest = {
        "scan_path": os.path.abspath(scan_path),
        "total_files_scanned": 0,
        "total_size_bytes": 0,
        "most_recent_modification_utc": None,
        "file_types": {}
    }

    most_recent_mod_timestamp = 0.0

    for root, _, files in os.walk(scan_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                file_size = os.path.getsize(file_path)
                file_mod_time = os.path.getmtime(file_path)

                manifest["total_files_scanned"] += 1
                manifest["total_size_bytes"] += file_size

                _, ext = os.path.splitext(file_name)
                ext = ext.lower() if ext else "[no_extension]"

                if ext not in manifest["file_types"]:
                    manifest["file_types"][ext] = {"count": 0, "total_size_bytes": 0}

                manifest["file_types"][ext]["count"] += 1
                manifest["file_types"][ext]["total_size_bytes"] += file_size

                if file_mod_time > most_recent_mod_timestamp:
                    most_recent_mod_timestamp = file_mod_time

            except OSError:
                # Ignore files that cannot be accessed (e.g., permission errors, broken symlinks)
                continue

    if most_recent_mod_timestamp > 0:
        dt_object = datetime.fromtimestamp(most_recent_mod_timestamp, tz=timezone.utc)
        manifest["most_recent_modification_utc"] = dt_object.isoformat(timespec='seconds').replace('+00:00', 'Z')

    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate a manifest of files in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to a file where the JSON output should be written. If not provided, output goes to stdout."
    )
    args = parser.parse_args()

    try:
        manifest = generate_manifest(args.path)
        json_output = json.dumps(manifest, indent=2)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"Manifest successfully written to {args.output}")
        else:
            print(json_output)
    except ValueError as e:
        print(f"Error: {e}", file=os.sys.stderr)
        os.sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.sys.stderr)
        os.sys.exit(1)

if __name__ == "__main__":
    main()
