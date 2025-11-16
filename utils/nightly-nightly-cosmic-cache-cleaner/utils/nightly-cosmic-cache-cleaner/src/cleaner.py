import os
import hashlib
import argparse
from datetime import datetime, timedelta

def get_file_hash(filepath, block_size=65536):
    """Generates MD5 hash for a given file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (OSError, IOError): # Handle cases where file might be inaccessible or unreadable
        return None # Return None for files that cannot be hashed

def find_old_files(directory, days_old):
    """Finds files in a directory older than a specified number of days."""
    old_files = []
    cutoff_date = datetime.now() - timedelta(days=days_old)

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)
                if mod_datetime < cutoff_date:
                    old_files.append(filepath)
            except OSError: # Handle cases where file might be inaccessible
                continue
    return old_files

def find_duplicate_files(directory):
    """Finds duplicate files in a directory based on MD5 hash."""
    hashes_to_paths = {}

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = get_file_hash(filepath)
            if file_hash is not None:
                if file_hash not in hashes_to_paths:
                    hashes_to_paths[file_hash] = []
                hashes_to_paths[file_hash].append(filepath)
    
    # Filter out groups with only one file (not true duplicates)
    duplicate_groups = [paths for paths in hashes_to_paths.values() if len(paths) > 1]
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Cache Cleaner: Identify old and duplicate files."
    )
    parser.add_argument(
        "--directory",
        required=True,
        help="The root directory to scan for cosmic debris."
    )
    parser.add_argument(
        "--days-old",
        type=int,
        default=90,
        help="Report files older than N days. (Default: 90)"
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Enable scanning for duplicate files based on content hash."
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        default=True, # Default to simulate for safety
        help="Only report findings; do not perform any deletion. (Default: True)"
    )

    args = parser.parse_args()

    print(f"\n--- Cosmic Cache Cleaner Report for '{args.directory}' ---")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Find old files
    print(f"\nScanning for files older than {args.days_old} days...")
    old_files = find_old_files(args.directory, args.days_old)
    if old_files:
        print(f"Found {len(old_files)} old files:")
        for f in old_files:
            print(f"  - {f}")
    else:
        print("No ancient cosmic relics found.")

    # Find duplicate files
    if args.find_duplicates:
        print("\nScanning for duplicate anomalies...")
        duplicate_groups = find_duplicate_files(args.directory)
        if duplicate_groups:
            print(f"Found {len(duplicate_groups)} groups of duplicate files:")
            for i, group in enumerate(duplicate_groups):
                print(f"  Group {i+1}:")
                for f in group:
                    print(f"    - {f}")
        else:
            print("No duplicate anomalies detected.")

    print("\n--- Scan Complete ---")
    if args.simulate:
        print("Note: This was a simulation. No files were modified or deleted.")

if __name__ == "__main__":
    main()
