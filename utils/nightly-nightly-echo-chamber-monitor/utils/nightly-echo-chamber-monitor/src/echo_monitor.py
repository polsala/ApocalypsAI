import os
import hashlib
import argparse
from collections import defaultdict

CHUNK_SIZE = 65536  # 64KB

def calculate_file_hash(filepath: str) -> str:
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Warning: Could not read file {filepath} - {e}")
        return ""

def find_duplicates(directory: str) -> dict[str, list[str]]:
    """
    Scans a directory for duplicate files based on their SHA256 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Error: Directory not found or is not a directory: {directory}")

    hashes: dict[str, list[str]] = defaultdict(list)
    print(f"Scanning '{directory}' for duplicate files...")

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hashes[file_hash].append(filepath)
    
    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Echo Chamber Monitor: Find duplicate files by content hash."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
    )

    args = parser.parse_args()

    try:
        duplicate_groups = find_duplicates(args.directory)

        if not duplicate_groups:
            print(f"No duplicate files found in '{args.directory}'. The echo chamber is clear!")
        else:
            print(f"\nFound {len(duplicate_groups)} groups of duplicate files:\n")
            for i, (file_hash, paths) in enumerate(duplicate_groups.items(), 1):
                print(f"Group {i} (SHA256: {file_hash[:12]}...{file_hash[-12:]}):")
                for path in paths:
                    print(f"  - {path}")
                print()

    except ValueError as e:
        print(e)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
