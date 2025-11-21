import os
import hashlib
import argparse
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file's content."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None
    return hasher.hexdigest()

def find_duplicate_files(directories):
    """Scans directories for duplicate files based on content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hashes = {}
    duplicates = {}

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not a directory: {directory}", file=sys.stderr)
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if not os.path.isfile(filepath):
                    continue # Skip if it's not a regular file (e.g., broken symlink)

                file_hash = calculate_file_hash(filepath)
                if file_hash is None:
                    continue

                if file_hash in hashes:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hashes[file_hash]] # Add the first file found
                    duplicates[file_hash].append(filepath)
                else:
                    hashes[file_hash] = filepath
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo-Chamber Auditor: Finds and optionally deletes duplicate files."
    )
    parser.add_argument(
        'directories', 
        metavar='directory', 
        type=str, 
        nargs='+',
        help='One or more directories to scan for duplicate files.'
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='If set, prompts for confirmation to delete duplicate files.'
    )

    args = parser.parse_args()

    print("\nScanning for echoes (duplicate files)...\n")
    duplicate_groups = find_duplicate_files(args.directories)

    if not duplicate_groups:
        print("No echoes found. Your digital space is pristine!")
        sys.exit(0)

    print("Echoes found!\n")
    total_deleted = 0
    for file_hash, paths in duplicate_groups.items():
        print(f"--- Hash: {file_hash} ---")
        print(f"  Original: {paths[0]}")
        for i, duplicate_path in enumerate(paths[1:]):
            print(f"  Duplicate {i+1}: {duplicate_path}")

            if args.delete:
                confirm = input(f"    Delete '{duplicate_path}'? (y/N): ").lower()
                if confirm == 'y':
                    try:
                        os.remove(duplicate_path)
                        print(f"    Deleted: {duplicate_path}")
                        total_deleted += 1
                    except OSError as e:
                        print(f"    Error deleting {duplicate_path}: {e}", file=sys.stderr)
                else:
                    print(f"    Skipped deletion of: {duplicate_path}")
        print()

    if args.delete:
        print(f"\nOperation complete. Total files deleted: {total_deleted}")
    else:
        print("\nTo delete duplicates, run with the --delete flag.")

    sys.exit(0)

if __name__ == '__main__':
    main()
