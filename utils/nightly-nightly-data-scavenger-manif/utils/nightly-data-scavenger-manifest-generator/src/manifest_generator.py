import os
import json
import argparse
from datetime import datetime, timezone

def generate_manifest(base_path: str, extensions: list[str]) -> list[dict]:
    """
    Scans a directory for files matching specified extensions and generates a manifest.

    Args:
        base_path: The root directory to start scanning from.
        extensions: A list of file extensions (without leading dots) to include.

    Returns:
        A list of dictionaries, each representing a file with its path, size, and last modified time.
    """
    manifest = []
    normalized_base_path = os.path.abspath(base_path)

    for root, _, files in os.walk(normalized_base_path):
        for file_name in files:
            if any(file_name.endswith(f'.{ext}') for ext in extensions):
                full_path = os.path.join(root, file_name)
                try:
                    # Get file stats
                    size_bytes = os.path.getsize(full_path)
                    mtime_timestamp = os.path.getmtime(full_path)

                    # Convert timestamp to ISO 8601 UTC string
                    dt_object = datetime.fromtimestamp(mtime_timestamp, tz=timezone.utc)
                    last_modified_utc = dt_object.isoformat(timespec='seconds').replace('+00:00', 'Z')

                    # Calculate relative path
                    relative_path = os.path.relpath(full_path, normalized_base_path)

                    manifest.append({
                        "path": relative_path,
                        "size_bytes": size_bytes,
                        "last_modified_utc": last_modified_utc
                    })
                except OSError as e:
                    # Skip files that cannot be accessed (e.g., broken symlinks, permission issues)
                    print(f"Warning: Could not access file {full_path}: {e}", file=os.stderr)
                    continue
    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate a data scavenger manifest for specified file types."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The base directory to start scanning from."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        required=True,
        help="Comma-separated list of file extensions (e.g., py,md,json)."
    )

    args = parser.parse_args()

    extensions_list = [ext.strip() for ext in args.extensions.split(',') if ext.strip()]

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' does not exist or is not a directory.", file=os.stderr)
        exit(1)

    manifest = generate_manifest(args.path, extensions_list)
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
