import os
import hashlib
import datetime
import argparse
import sys

def get_file_hash(filepath, block_size=65536):
    """Generates an MD5 hash for a given file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files

def find_dust_bunnies(root_dir, age_threshold_days=None, detect_duplicates=False):
    """
    Scans a directory for old and/or duplicate files.

    Args:
        root_dir (str): The path to the directory to scan.
        age_threshold_days (int, optional): Files older than this many days are considered old.
        detect_duplicates (bool): If True, detect duplicate files by content hash.

    Returns:
        dict: A dictionary containing lists of 'old_files' and 'duplicate_files'.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.", file=sys.stderr)
        return {'old_files': [], 'duplicate_files': []}

    old_files = []
    file_hashes = {} # hash -> [filepath1, filepath2, ...]
    current_time = datetime.datetime.now()

    print(f"Scanning '{root_dir}' for dust bunnies...")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            if not os.path.isfile(filepath):
                continue # Skip if it's not a regular file (e.g., broken symlink)

            # Check for old files
            if age_threshold_days is not None:
                try:
                    mtime_timestamp = os.path.getmtime(filepath)
                    mtime_datetime = datetime.datetime.fromtimestamp(mtime_timestamp)
                    age = current_time - mtime_datetime
                    if age.days > age_threshold_days:
                        old_files.append(filepath)
                except OSError:
                    # Handle files with inaccessible modification times
                    pass

            # Check for duplicates
            if detect_duplicates:
                file_hash = get_file_hash(filepath)
                if file_hash:
                    if file_hash not in file_hashes:
                        file_hashes[file_hash] = []
                    file_hashes[file_hash].append(filepath)

    duplicate_files = {
        h: paths for h, paths in file_hashes.items() if len(paths) > 1
    }

    return {
        'old_files': old_files,
        'duplicate_files': duplicate_files
    }

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Dust-Bunny Detector: Scans directories for old and/or duplicate files."
    )
    parser.add_argument(
        "directory_path",
        help="The root directory to scan."
    )
    parser.add_argument(
        "--age",
        type=int,
        metavar="DAYS",
        help="Detect files older than this many days."
    )
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Detect duplicate files based on content hash."
    )

    args = parser.parse_args()

    if not args.age and not args.duplicates:
        print("Please specify at least one detection method: --age <DAYS> or --duplicates.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    results = find_dust_bunnies(args.directory_path, args.age, args.duplicates)

    print("\n--- Dust Bunny Detection Report ---")

    if results['old_files']:
        print(f"\nFound {len(results['old_files'])} old files (older than {args.age} days):")
        for f in results['old_files']:
            print(f"  - {f}")
    elif args.age is not None:
        print(f"\nNo files found older than {args.age} days.")

    if results['duplicate_files']:
        print(f"\nFound {len(results['duplicate_files'])} sets of duplicate files:")
        for file_hash, paths in results['duplicate_files'].items():
            print(f"  Hash: {file_hash[:8]}...")
            for p in paths:
                print(f"    - {p}")
    elif args.duplicates:
        print("\nNo duplicate files found.")

    if not results['old_files'] and not results['duplicate_files']:
        print("\nCongratulations! No dust bunnies detected. Your digital space is sparkling clean.")
    else:
        print("\nConsider reviewing the detected files for cleanup.")

if __name__ == "__main__":
    main()
