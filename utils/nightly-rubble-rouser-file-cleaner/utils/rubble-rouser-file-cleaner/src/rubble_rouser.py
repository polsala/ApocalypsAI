import os
import hashlib
import argparse
from collections import defaultdict

def find_empty_dirs(path):
    """
    Finds all empty directories within the given path.
    A directory is considered empty if it contains no files and no subdirectories.
    """
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def _hash_file(filepath, block_size=65536):
    """Generates MD5 hash for a given file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicate_files(path, verbose=False):
    """
    Finds all duplicate files within the given path based on their MD5 hash.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symlinks to avoid issues
                continue
            try:
                file_hash = _hash_file(filepath)
                hashes[file_hash].append(filepath)
                if verbose:
                    print(f"Hashed: {filepath}")
            except IOError as e:
                if verbose:
                    print(f"Warning: Could not read file {filepath} - {e}")
                continue
    
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Rubble-Rouser File Cleaner: Clear the digital wasteland!"
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--find-empty-dirs",
        action="store_true",
        help="Enable scanning for empty directories."
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Enable scanning for duplicate files."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed output during scanning."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"--- Rubble-Rouser Scan Report for '{args.path}' ---")

    if args.find_empty_dirs:
        print("\nScanning for empty directories...")
        empty_dirs = find_empty_dirs(args.path)
        if empty_dirs:
            print(f"Found {len(empty_dirs)} empty directories:")
            for d in empty_dirs:
                print(f"  - {d}")
        else:
            print("No empty directories found. Your digital shelter is tidy!")

    if args.find_duplicates:
        print("\nScanning for duplicate files...")
        duplicates = find_duplicate_files(args.path, args.verbose)
        if duplicates:
            total_duplicates = sum(len(files) - 1 for files in duplicates.values())
            print(f"Found {total_duplicates} duplicate files across {len(duplicates)} unique sets:")
            for file_hash, files in duplicates.items():
                print(f"  Hash: {file_hash}")
                for f in files:
                    print(f"    - {f}")
        else:
            print("No duplicate files found. Your scavenged treasures are unique!")

    print("\n--- Scan Complete ---")

if __name__ == "__main__":
    main()
