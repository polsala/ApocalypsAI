import os
import hashlib
import json
from datetime import datetime

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
    except IOError as e:
        raise IOError(f"Could not read file {filepath}: {e}") from e
    return sha256.hexdigest()

def record_directory_snapshot(target_dir, output_file):
    """
    Records a snapshot of the target directory's structure and file hashes.
    The snapshot includes relative path, SHA256 hash, size, and last modification time.
    """
    if not os.path.isdir(target_dir):
        raise FileNotFoundError(f"Target directory not found: {target_dir}")

    snapshot_data = {
        "timestamp": datetime.now().isoformat(),
        "target_directory": os.path.abspath(target_dir),
        "files": []
    }

    for root, _, files in os.walk(target_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, target_dir)
            try:
                file_hash = calculate_file_hash(filepath)
                file_size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                snapshot_data["files"].append({
                    "path": relative_path,
                    "hash": file_hash,
                    "size": file_size,
                    "mtime": datetime.fromtimestamp(mtime).isoformat()
                })
            except (IOError, OSError) as e:
                print(f"Warning: Could not process file {filepath}: {e}")
                # Continue processing other files even if one fails

    with open(output_file, 'w') as f:
        json.dump(snapshot_data, f, indent=2)
    
    return snapshot_data

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Record a snapshot of a directory's files and their hashes."
    )
    parser.add_argument("target_directory", help="The directory to snapshot.")
    parser.add_argument("output_file", help="The JSON file to save the snapshot to.")
    
    args = parser.parse_args()

    try:
        print(f"Recording snapshot for '{args.target_directory}' to '{args.output_file}'...")
        snapshot = record_directory_snapshot(args.target_directory, args.output_file)
        print(f"Snapshot recorded successfully with {len(snapshot['files'])} files.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
