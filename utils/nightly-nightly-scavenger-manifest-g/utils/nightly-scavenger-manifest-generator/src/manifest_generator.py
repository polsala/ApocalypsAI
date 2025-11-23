import os
import json
import hashlib
import argparse
from datetime import datetime, timezone
from fnmatch import fnmatch

def get_file_checksum(filepath, hash_algo=hashlib.sha256, chunk_size=8192):
    """Calculates the SHA256 checksum of a file."""
    hasher = hash_algo()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
    except OSError as e:
        # Handle cases where file might be inaccessible during checksum calculation
        raise OSError(f"Failed to read file for checksum: {filepath} - {e}") from e
    return hasher.hexdigest()

def generate_manifest(
    directory_path,
    output_filename='manifest.json',
    recursive=False,
    exclude_patterns=None
):
    """Scans a directory and generates a JSON manifest of its files."""
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    manifest = {
        "manifest_version": "1.0",
        "scan_timestamp": datetime.now(timezone.utc).isoformat(timespec='seconds'),
        "scanned_directory": os.path.abspath(directory_path),
        "files": []
    }

    exclude_patterns = exclude_patterns or []

    for root, dirs, files in os.walk(directory_path):
        # Calculate relative path for current root
        relative_root = os.path.relpath(root, directory_path)
        if relative_root == '.':
            relative_root = ''

        # Filter out excluded directories if not recursive or if pattern matches
        if not recursive and relative_root != '':
            dirs.clear() # Don't recurse into subdirectories
            continue

        # Apply exclude patterns to directories for recursive scans
        dirs_to_keep = []
        for d in list(dirs):
            full_relative_path = os.path.join(relative_root, d)
            # Check if the directory itself or its contents should be excluded
            if not any(fnmatch(full_relative_path, p) or fnmatch(os.path.join(full_relative_path, '*'), p) for p in exclude_patterns):
                dirs_to_keep.append(d)
        dirs[:] = dirs_to_keep # Modify dirs in-place for os.walk

        for filename in files:
            filepath = os.path.join(root, filename)
            relative_filepath = os.path.join(relative_root, filename)

            # Apply exclude patterns to files
            if any(fnmatch(relative_filepath, p) for p in exclude_patterns):
                continue

            try:
                stat_info = os.stat(filepath)
                size_bytes = stat_info.st_size
                last_modified_utc = datetime.fromtimestamp(stat_info.st_mtime, tz=timezone.utc).isoformat(timespec='seconds')
                sha256_checksum = get_file_checksum(filepath)

                manifest["files"].append({
                    "path": relative_filepath,
                    "name": filename,
                    "size_bytes": size_bytes,
                    "last_modified_utc": last_modified_utc,
                    "sha256_checksum": sha256_checksum
                })
            except OSError as e:
                print(f"Warning: Could not process file {filepath}: {e}")
                continue

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest generated successfully: {output_filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a JSON manifest of files in a directory."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="manifest.json",
        help="The name of the output JSON file. Defaults to 'manifest.json'."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        help="Comma-separated glob patterns (e.g., '*.log,temp/*') to exclude files or directories."
    )

    args = parser.parse_args()

    exclude_patterns = []
    if args.exclude:
        exclude_patterns = [p.strip() for p in args.exclude.split(',') if p.strip()]

    try:
        generate_manifest(
            args.directory_path,
            output_filename=args.output,
            recursive=args.recursive,
            exclude_patterns=exclude_patterns
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
