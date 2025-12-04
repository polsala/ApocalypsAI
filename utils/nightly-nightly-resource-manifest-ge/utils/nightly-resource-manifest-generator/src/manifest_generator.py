import os
import hashlib
import json
import yaml
import argparse
from datetime import datetime

def calculate_file_hash(filepath, hash_algorithm='sha256'):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def generate_manifest(root_dir):
    """Scans a directory and generates a list of file metadata."""
    manifest_entries = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                relative_path = os.path.relpath(filepath, root_dir)
                size_bytes = os.path.getsize(filepath)
                sha256_hash = calculate_file_hash(filepath)
                # Using isoformat() and appending 'Z' for UTC representation. 
                # Assumes getmtime returns a UTC timestamp or that local time is handled consistently.
                last_modified_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat() + 'Z'

                manifest_entries.append({
                    "path": relative_path,
                    "size_bytes": size_bytes,
                    "sha256_hash": sha256_hash,
                    "last_modified_timestamp": last_modified_timestamp
                })
            except OSError as e:
                print(f"Warning: Could not process {filepath}: {e}")
                continue
    
    # Using isoformat() and appending 'Z' for UTC representation.
    scan_timestamp = datetime.now().isoformat() + 'Z'
    return {
        "scan_root": os.path.abspath(root_dir),
        "scan_timestamp": scan_timestamp,
        "files": manifest_entries
    }

def main():
    parser = argparse.ArgumentParser(
        description="Generate a resource manifest for a given directory."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The root directory to scan for resources."
    )
    parser.add_argument(
        "--output-format", 
        choices=['json', 'yaml'], 
        required=True, 
        help="The desired output format (json or yaml)."
    )
    parser.add_argument(
        "--output-file", 
        help="Optional. If provided, the manifest will be written to this file. Otherwise, it prints to stdout."
    )

    args = parser.parse_args()

    manifest = generate_manifest(args.path)

    output_content = ""
    if args.output_format == 'json':
        output_content = json.dumps(manifest, indent=2)
    elif args.output_format == 'yaml':
        # sort_keys=False to maintain insertion order for better readability in YAML
        output_content = yaml.dump(manifest, indent=2, sort_keys=False)

    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output_content)
        print(f"Manifest successfully written to {args.output_file}")
    else:
        print(output_content)

if __name__ == "__main__":
    main()
