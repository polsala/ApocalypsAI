import os
import hashlib
import json
import argparse
from datetime import datetime

def calculate_sha256(filepath: str) -> str:
    """Calculates the SHA256 hash of a given file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return "ERROR"

def generate_manifest(root_dir: str) -> dict:
    """Generates a manifest of files in a directory with their SHA256 hashes and sizes."""
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "root_path": os.path.abspath(root_dir),
        "files": []
    }
    
    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}")
        return manifest

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(filepath, root_dir)
            try:
                file_size = os.path.getsize(filepath)
                file_hash = calculate_sha256(filepath)
                manifest["files"].append({
                    "path": relative_path,
                    "size": file_size,
                    "sha256": file_hash
                })
            except OSError as e:
                print(f"Warning: Could not process {filepath}: {e}")
                manifest["files"].append({
                    "path": relative_path,
                    "size": -1, # Indicate error
                    "sha256": "ERROR"
                })
    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate a data integrity manifest for a directory."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to scan."
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="manifest.json", 
        help="The output JSON file name."
    )
    
    args = parser.parse_args()
    
    manifest_data = generate_manifest(args.path)
    
    try:
        with open(args.output, 'w') as f:
            json.dump(manifest_data, f, indent=2)
        print(f"Manifest successfully generated and saved to {args.output}")
    except IOError as e:
        print(f"Error writing manifest to {args.output}: {e}")

if __name__ == "__main__":
    main()
