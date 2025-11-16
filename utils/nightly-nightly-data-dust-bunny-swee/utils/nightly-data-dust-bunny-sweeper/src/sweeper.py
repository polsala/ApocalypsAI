import os
import hashlib
import argparse
import sys
from datetime import datetime, timedelta

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file's content."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicates(root_dir):
    """Finds duplicate files by comparing their MD5 hashes."""
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.isfile(filepath): # Skip if it's not a file (e.g., broken symlink)
                continue
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                if file_hash in hashes:
                    duplicates.append((filepath, hashes[file_hash]))
                else:
                    hashes[file_hash] = filepath
    return duplicates

def find_empty_dirs(root_dir):
    """Finds empty directories within the given root directory."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # If a directory has no files and no subdirectories, it's empty
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_old_files(root_dir, age_days):
    """Finds files older than a specified number of days."""
    old_files = []
    cutoff_date = datetime.now() - timedelta(days=age_days)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.isfile(filepath): # Skip if not a file
                continue
            try:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                if mtime_datetime < cutoff_date:
                    old_files.append(filepath)
            except OSError: # Handle files with inaccessible metadata
                continue
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: find and optionally remove duplicate files, empty directories, and old files."
    )
    parser.add_argument('--path', type=str, required=True,
                        help='The root directory to scan.')
    parser.add_argument('--duplicates', action='store_true',
                        help='Find duplicate files.')
    parser.add_argument('--empty-dirs', action='store_true',
                        help='Find empty directories.')
    parser.add_argument('--old-files', type=int, metavar='DAYS',
                        help='Find files older than DAYS.')
    parser.add_argument('--delete', action='store_true',
                        help='WARNING: Delete found items. Use with caution! (Default: list only)')

    args = parser.parse_args()

    if not any([args.duplicates, args.empty_dirs, args.old_files]):
        print("Error: Please specify at least one operation (--duplicates, --empty-dirs, or --old-files).")
        parser.print_help()
        sys.exit(1)

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{args.path}' for digital dust bunnies...")

    if args.duplicates:
        print("\n--- Duplicate Files ---")
        dupes = find_duplicates(args.path)
        if dupes:
            for i, (file1, file2) in enumerate(dupes):
                print(f"  {i+1}. Duplicate pair: '{file1}' and '{file2}'")
                if args.delete:
                    try:
                        os.remove(file1) # Only remove one of the duplicates
                        print(f"     Deleted '{file1}'")
                    except OSError as e:
                        print(f"     Error deleting '{file1}': {e}")
            print(f"Found {len(dupes)} duplicate pairs.")
        else:
            print("  No duplicate files found.")

    if args.empty_dirs:
        print("\n--- Empty Directories ---")
        empty_dirs = find_empty_dirs(args.path)
        if empty_dirs:
            for i, d in enumerate(empty_dirs):
                print(f"  {i+1}. Empty directory: '{d}'")
                if args.delete:
                    try:
                        os.rmdir(d)
                        print(f"     Deleted '{d}'")
                    except OSError as e:
                        print(f"     Error deleting '{d}': {e}")
            print(f"Found {len(empty_dirs)} empty directories.")
        else:
            print("  No empty directories found.")

    if args.old_files is not None:
        print(f"\n--- Files Older Than {args.old_files} Days ---")
        old_files = find_old_files(args.path, args.old_files)
        if old_files:
            for i, f in enumerate(old_files):
                print(f"  {i+1}. Old file: '{f}'")
                if args.delete:
                    try:
                        os.remove(f)
                        print(f"     Deleted '{f}'")
                    except OSError as e:
                        print(f"     Error deleting '{f}': {e}")
            print(f"Found {len(old_files)} old files.")
        else:
            print("  No old files found.")

    print("\nDigital dust bunny sweep complete!")

if __name__ == '__main__':
    main()
