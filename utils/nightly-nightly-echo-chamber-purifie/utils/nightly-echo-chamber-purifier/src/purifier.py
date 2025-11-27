import hashlib
import os
import argparse
from collections import defaultdict
from pathlib import Path

def calculate_file_hash(filepath: Path) -> str:
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directories: list[Path]) -> dict[str, list[Path]]:
    """
    Scans specified directories for duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that correspond to more than one file.
    """
    file_hashes: defaultdict[str, list[Path]] = defaultdict(list)
    
    for directory in directories:
        if not directory.is_dir():
            print(f"Warning: Directory not found or not a directory: {directory}")
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = Path(root) / filename
                try:
                    file_hash = calculate_file_hash(filepath)
                    file_hashes[file_hash].append(filepath)
                except OSError as e:
                    print(f"Error processing file {filepath}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred with file {filepath}: {e}")

    duplicates = {
        h: paths for h, paths in file_hashes.items() if len(paths) > 1
    }
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo-Chamber Purifier: Scans directories for duplicate files."
    )
    parser.add_argument(
        "directories",
        nargs=":",
        type=Path,
        help="One or more directories to scan for duplicate files."
    )
    args = parser.parse_args()

    if not args.directories:
        print("Error: No directories provided. Please specify at least one directory to scan.")
        parser.print_help()
        exit(1)

    print("🌌 Initiating Nightly Echo-Chamber Purification... 🌌")
    print(f"Scanning directories: {[str(d) for d in args.directories]}")

    duplicates = find_duplicates(args.directories)

    if not duplicates:
        print("\n✨ No echoes found! Your digital chambers are pristine. ✨")
    else:
        print("\n🚨 Echoes detected! Duplicate files found: 🚨")
        for file_hash, paths in duplicates.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")
        print("\nConsider consolidating or removing redundant files to purify your repository.")

if __name__ == "__main__":
    main()
