import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm=hashlib.sha256, chunk_size=4096):
    """Calculates the hash of a file."""
    hasher = hash_algorithm()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicate_files(paths):
    """
    Scans specified paths for duplicate files based on their SHA256 hash.

    Args:
        paths (list): A list of directory paths or file paths to scan.

    Returns:
        dict: A dictionary where keys are file hashes and values are dictionaries
              containing 'size' and 'files' (list of file paths) for duplicate sets.
              Only includes hashes with more than one file.
    """
    file_hashes = defaultdict(list)
    file_sizes = {} # Store size for reporting

    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found - {path}", file=sys.stderr)
            continue

        if os.path.isfile(path):
            try:
                size = os.path.getsize(path)
                file_sizes[path] = size
                file_hash = calculate_file_hash(path)
                if file_hash:
                    file_hashes[file_hash].append(path)
            except OSError as e:
                print(f"Error accessing file {path}: {e}", file=sys.stderr)
            continue

        for root, _, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    # Skip symlinks to avoid infinite loops or external files unless explicitly handled
                    if os.path.islink(filepath):
                        continue
                    size = os.path.getsize(filepath)
                    file_sizes[filepath] = size
                    file_hash = calculate_file_hash(filepath)
                    if file_hash:
                        file_hashes[file_hash].append(filepath)
                except OSError as e:
                    print(f"Error accessing file {filepath}: {e}", file=sys.stderr)
                    continue

    duplicates = {
        h: files for h, files in file_hashes.items() if len(files) > 1
    }

    # Add file sizes to the duplicate report for convenience
    duplicate_report = {}
    for h, files in duplicates.items():
        # All files in a duplicate group will have the same size
        # Use the size of the first file found for this hash
        size = file_sizes.get(files[0], 0)
        duplicate_report[h] = {'size': size, 'files': files}

    return duplicate_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/echo_locator.py <path1> [path2 ...]")
        sys.exit(1)

    paths_to_scan = sys.argv[1:]
    duplicate_report = find_duplicate_files(paths_to_scan)

    if not duplicate_report:
        print("No duplicate files found. Your digital wasteland is pristine!")
        sys.exit(0)

    print("--- Duplicate Files Report ---")
    for file_hash, data in duplicate_report.items():
        print(f"\n--- Duplicate Group (SHA256: {file_hash}) ---")
        print(f"  Size: {data['size']} bytes")
        for filepath in data['files']:
            print(f"  - {filepath}")
    print("\n--- End of Report ---")

if __name__ == "__main__":
    main()
