import os
import hashlib
import argparse
import sys
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except FileNotFoundError:
        # File might be deleted or inaccessible between os.walk and open
        return None 
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(paths):
    """
    Scans given paths for duplicate files based on their MD5 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one file associated (i.e., duplicates).
    """
    file_hashes = defaultdict(list)
    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path '{path}' does not exist. Skipping.", file=sys.stderr)
            continue

        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                # Skip directories and non-regular files (e.g., symlinks pointing to non-files)
                if not os.path.isfile(filepath):
                    continue
                
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    file_hashes[file_hash].append(filepath)
    
    duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Monitor: Find duplicate files based on content hash."
    )
    parser.add_argument(
        'paths',
        metavar='PATH',
        type=str,
        nargs='+',
        help='One or more directories to scan for duplicate files.'
    )
    args = parser.parse_args()

    print("Scanning for duplicate files...")
    duplicates = find_duplicate_files(args.paths)

    if duplicates:
        print("\n--- Duplicate Files Found ---")
        for hash_val, files in duplicates.items():
            print(f"\nHash: {hash_val}")
            for f in files:
                print(f"  - {f}")
        print("\n--- End of Duplicates ---")
        sys.exit(0) # Indicate duplicates were found
    else:
        print("\nNo duplicate files found.")
        sys.exit(2) # Indicate no duplicates (no-op)

if __name__ == '__main__':
    main()
