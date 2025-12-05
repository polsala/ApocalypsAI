import os
import hashlib
import argparse
from collections import defaultdict

CHUNK_SIZE = 65536 # 64KB

def calculate_file_hash(filepath, hash_algo='sha256'):
    """Calculates the SHA256 hash of a file in chunks."""
    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def find_duplicates(directory, hash_algo='sha256'):
    """Scans a directory for duplicate files based on their content hash.

    Returns a dictionary where keys are file hashes and values are lists of file paths
    that share that hash, but only for hashes that appear more than once.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid issues or unintended hashing
                continue
            try:
                file_hash = calculate_file_hash(filepath, hash_algo)
                if file_hash:
                    hashes[file_hash].append(filepath)
            except Exception as e:
                print(f"Warning: Could not process {filepath}: {e}")

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Quantum Quake Deduplicator: Find and optionally remove duplicate files."
    )
    parser.add_argument(
        'directory',
        type=str,
        help='The path to the directory to scan for duplicates.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a scan and report duplicates, but do not delete any files.'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='After identifying duplicates, prompt to confirm deletion of all but one instance of each duplicate set.'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        exit(1)

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicates = find_duplicates(args.directory)

    if not duplicates:
        print("No duplicate files found. Your data hoard is pristine!")
        exit(0)

    print(f"Found {len(duplicates)} sets of duplicate files:")
    total_deleted_size = 0
    files_to_delete_count = 0

    for file_hash, paths in duplicates.items():
        print(f"\nHash: {file_hash}")
        print(f"  Original (kept): {paths[0]}")
        for i, duplicate_path in enumerate(paths[1:]):
            print(f"  Duplicate {i+1} (to {'delete' if args.delete else 'report'}): {duplicate_path}")
            if args.delete or args.dry_run:
                try:
                    filesize = os.path.getsize(duplicate_path)
                    total_deleted_size += filesize
                    files_to_delete_count += 1
                except FileNotFoundError:
                    print(f"    Warning: File not found during size check: {duplicate_path}")

    if args.dry_run or not args.delete:
        print("\n--- Dry Run Complete ---")
        if files_to_delete_count > 0:
            print(f"If --delete were used, {files_to_delete_count} files (totaling {total_deleted_size / (1024*1024):.2f} MB) would be deleted.")
        else:
            print("No files would be deleted.")
        print("No files were modified or deleted.")
    elif args.delete:
        print(f"\nFound {files_to_delete_count} duplicate files (totaling {total_deleted_size / (1024*1024):.2f} MB) that can be deleted.")
        confirmation = input("Proceed with deleting these files? (y/N): ").strip().lower()
        if confirmation == 'y':
            deleted_count = 0
            for file_hash, paths in duplicates.items():
                for duplicate_path in paths[1:]:
                    try:
                        os.remove(duplicate_path)
                        print(f"Deleted: {duplicate_path}")
                        deleted_count += 1
                    except OSError as e:
                        print(f"Error deleting {duplicate_path}: {e}")
            print(f"\nSuccessfully deleted {deleted_count} duplicate files.")
        else:
            print("Deletion cancelled. No files were deleted.")


if __name__ == '__main__':
    main()
