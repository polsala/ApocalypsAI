import hashlib
import os
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """
    Scans a directory for duplicate files based on their SHA256 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file path associated (duplicates).
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symlinks to avoid issues
                continue
            try:
                file_hash = calculate_file_hash(filepath)
                hashes[file_hash].append(filepath)
            except IOError as e:
                print(f"Warning: Could not read file {filepath}: {e}")
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")
    
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Scan a directory for duplicate files based on content hash."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist or is not a directory.")
        exit(1)

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicate_groups = find_duplicate_files(args.directory)

    if not duplicate_groups:
        print("No duplicate files found. Your data debris is pristine!")
    else:
        print("\n--- Duplicate File Groups Found ---")
        for file_hash, paths in duplicate_groups.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")
        print("\n--- End of Duplicates ---")
        print(f"Found {len(duplicate_groups)} groups of duplicate files.")

if __name__ == "__main__":
    main()
