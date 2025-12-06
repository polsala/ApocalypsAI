import os
import hashlib
import argparse
import sys
import datetime
import time

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_duplicates(path):
    """Finds duplicate files in the given path based on their MD5 hash.
    Returns a list of all file paths that are part of a duplicate group.
    """
    print(f"\nScanning '{path}' for duplicate files...")
    hashes = {}
    all_duplicate_paths = []
    
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                try:
                    file_hash = calculate_file_hash(filepath)
                    if file_hash in hashes:
                        # If hash already seen, add current file and the previously seen file(s) to duplicates
                        if hashes[file_hash] not in all_duplicate_paths: # Add the first instance if not already added
                            all_duplicate_paths.append(hashes[file_hash])
                        all_duplicate_paths.append(filepath)
                    else:
                        hashes[file_hash] = filepath # Store the first instance of this hash
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}", file=sys.stderr)
    
    if not all_duplicate_paths:
        print("No duplicate files found.")
        return []

    # For output, group them by hash for readability
    grouped_duplicates = {}
    for filepath in all_duplicate_paths:
        try:
            file_hash = calculate_file_hash(filepath) # Recalculate hash for grouping
            grouped_duplicates.setdefault(file_hash, []).append(filepath)
        except Exception as e:
            print(f"Error re-hashing file {filepath} for grouping: {e}", file=sys.stderr)

    print("Found duplicate files:")
    for file_hash, files in grouped_duplicates.items():
        print(f"  Hash: {file_hash}")
        for f in files:
            print(f"    - {f}")
    
    return all_duplicate_paths

def find_empty_dirs(path):
    """Finds empty directories in the given path."""
    print(f"\nScanning '{path}' for empty directories...")
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        # Check if current directory is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    
    if not empty_dirs:
        print("No empty directories found.")
        return []

    print("Found empty directories:")
    for d in empty_dirs:
        print(f"  - {d}")
    return empty_dirs

def find_old_files(path, days_old):
    """Finds files older than 'days_old' in the given path."""
    print(f"\nScanning '{path}' for files older than {days_old} days...")
    old_files = []
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath) and not os.path.islink(filepath):
                try:
                    mtime = os.path.getmtime(filepath)
                    if mtime < cutoff_time:
                        old_files.append(filepath)
                except Exception as e:
                    print(f"Error checking file {filepath}: {e}", file=sys.stderr)
    
    if not old_files:
        print(f"No files found older than {days_old} days.")
        return []

    print(f"Found files older than {days_old} days:")
    for f in old_files:
        print(f"  - {f}")
    return old_files

def delete_items(items, item_type):
    """Deletes a list of files or directories."""
    print(f"\nAttempting to delete {len(items)} {item_type}(s)...")
    deleted_count = 0
    for item in items:
        try:
            if os.path.isfile(item):
                os.remove(item)
                print(f"  Deleted file: {item}")
            elif os.path.isdir(item):
                os.rmdir(item)
                print(f"  Deleted empty directory: {item}")
            deleted_count += 1
        except OSError as e:
            print(f"  Error deleting {item_type} {item}: {e}", file=sys.stderr)
    print(f"Successfully deleted {deleted_count} out of {len(items)} {item_type}(s).")

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical-yet-useful Python utility to reclaim disk space."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to scan (default: current directory)."
    )
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Find and list duplicate files."
    )
    parser.add_argument(
        "--empty-dirs",
        action="store_true",
        help="Find and list empty directories."
    )
    parser.add_argument(
        "--old-files",
        type=int,
        metavar='DAYS_OLD',
        help="Find and list files older than DAYS_OLD days."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="WARNING: Actually delete the identified files/directories. Use with extreme caution."
    )

    args = parser.parse_args()

    if not (args.duplicates or args.empty_dirs or args.old_files):
        print("Please specify at least one action: --duplicates, --empty-dirs, or --old-files.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    scan_path = os.path.abspath(args.path)
    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    all_items_to_delete = []

    if args.duplicates:
        dupes = find_duplicates(scan_path)
        if args.delete:
            all_items_to_delete.extend(dupes)

    if args.empty_dirs:
        empty_directories = find_empty_dirs(scan_path)
        if args.delete:
            all_items_to_delete.extend(empty_directories)

    if args.old_files is not None:
        old_files_list = find_old_files(scan_path, args.old_files)
        if args.delete:
            all_items_to_delete.extend(old_files_list)
    
    if args.delete and all_items_to_delete:
        # Remove duplicates from the list of items to delete, if any item was found by multiple criteria
        all_items_to_delete = list(set(all_items_to_delete))
        delete_items(all_items_to_delete, "item")
    elif args.delete and not all_items_to_delete:
        print("No items found for deletion.")

if __name__ == "__main__":
    main()
