import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo=hashlib.sha256, block_size=65536):
    """Calculates the SHA256 hash of a file's content."""
    hasher = hash_algo()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        # Handle cases where file might be inaccessible or disappear during scan
        return None

def find_duplicate_files(directories, dry_run=True):
    """
    Scans specified directories for duplicate files based on content hash.

    Args:
        directories (list): A list of directory paths to scan.
        dry_run (bool): If True, only report duplicates; otherwise, could implement deletion (not implemented here).

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of file paths
              that share that hash (i.e., are duplicates).
    """
    files_by_size = defaultdict(list)
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not accessible: {directory}", file=sys.stderr)
            continue

        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    # Use stat to get size, faster than opening file
                    file_size = os.path.getsize(filepath)
                    files_by_size[file_size].append(filepath)
                except OSError:
                    # File might be a broken symlink, inaccessible, etc.
                    continue

    duplicate_hashes = defaultdict(list)
    for size, filepaths in files_by_size.items():
        if len(filepaths) < 2:
            continue # No duplicates possible for this size

        hashes = {}
        for filepath in filepaths:
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                if file_hash in hashes:
                    # If this hash is already seen, it's a duplicate
                    # Add all paths that share this hash to the duplicate_hashes dict
                    if file_hash not in duplicate_hashes:
                        duplicate_hashes[file_hash].append(hashes[file_hash]) # Add the first path
                    duplicate_hashes[file_hash].append(filepath) # Add the current path
                else:
                    hashes[file_hash] = filepath # Store the first path for this hash

    return duplicate_hashes

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/duster.py <directory1> [directory2 ...] [--dry-run]", file=sys.stderr)
        sys.exit(1)

    directories = []
    dry_run = True

    for arg in sys.argv[1:]:
        if arg == "--dry-run":
            dry_run = True
        else:
            directories.append(arg)

    if not directories:
        print("Error: No directories specified for scanning.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning directories: {', '.join(directories)}")
    print(f"Mode: {'Dry Run' if dry_run else 'Live (deletion not implemented)'}")

    duplicates = find_duplicate_files(directories, dry_run=dry_run)

    if duplicates:
        print("\n--- Duplicate Files Found ---")
        total_potential_space_saved = 0
        for file_hash, filepaths in duplicates.items():
            # Get size from the first file path (all duplicates have same size)
            try:
                file_size = os.path.getsize(filepaths[0])
                # Space saved is (N-1) * size, where N is number of duplicates
                potential_saved_for_group = (len(filepaths) - 1) * file_size
                total_potential_space_saved += potential_saved_for_group

                print(f"\nHash: {file_hash}")
                print(f"Size: {file_size / (1024*1024):.2f} MB (each)")
                for path in filepaths:
                    print(f"  - {path}")
            except OSError:
                print(f"\nHash: {file_hash} (Error getting size for some paths)")
                for path in filepaths:
                    print(f"  - {path}")

        print("\n-----------------------------")
        print(f"Total potential space reclaimable: {total_potential_space_saved / (1024*1024):.2f} MB")
        print("-----------------------------")
    else:
        print("\nNo duplicate files found. Your digital realm is pristine!")

if __name__ == "__main__":
    main()
