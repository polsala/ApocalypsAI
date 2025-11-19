import os
import hashlib
import argparse
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # File might be inaccessible or disappear during scan

def find_duplicates(directory):
    """Finds duplicate files in the given directory.

    Returns a tuple: (duplicates_dict, total_potential_savings_bytes)
    duplicates_dict: A dictionary where keys are SHA256 hashes and values are lists of
    file paths that share that hash, but only for hashes with more than one file.
    """
    files_by_size = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                try:
                    file_size = os.path.getsize(filepath)
                    if file_size not in files_by_size:
                        files_by_size[file_size] = []
                    files_by_size[file_size].append(filepath)
                except (OSError, FileNotFoundError):
                    # File might be inaccessible or disappear during scan
                    continue

    duplicates = {}
    total_potential_savings = 0

    for size, filepaths in files_by_size.items():
        if len(filepaths) < 2: # No duplicates if only one file of this size
            continue

        files_by_hash = {}
        for filepath in filepaths:
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                if file_hash not in files_by_hash:
                    files_by_hash[file_hash] = []
                files_by_hash[file_hash].append(filepath)
        
        for file_hash, paths in files_by_hash.items():
            if len(paths) > 1:
                duplicates[file_hash] = paths
                # Calculate potential savings for this group
                total_potential_savings += size * (len(paths) - 1)

    return duplicates, total_potential_savings

def format_bytes(bytes_value):
    """Formats a byte value into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} EB" # Just in case, for Exabytes

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally remove duplicate files in a directory."
    )
    parser.add_argument(
        "--directory", 
        required=True, 
        help="The root directory to scan for duplicate files."
    )
    parser.add_argument(
        "--delete", 
        action="store_true", 
        help="If provided, deletes all but one instance of each duplicate group. Use with caution!"
    )

    args = parser.parse_args()
    target_directory = os.path.abspath(args.directory)

    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{target_directory}' for duplicate files...")
    duplicates, total_potential_savings = find_duplicates(target_directory)

    if not duplicates:
        print("No duplicate files found. Your echo chamber is pristine!")
        sys.exit(0)

    print("\n--- Duplicate Files Found ---")
    deleted_count = 0
    deleted_size = 0

    for file_hash, paths in duplicates.items():
        print(f"\nHash: {file_hash}")
        print(f"  Original (keeping): {paths[0]}")
        for i, path in enumerate(paths[1:]):
            print(f"  Duplicate {i+1}: {path}")

    print(f"\nTotal potential space savings: {format_bytes(total_potential_savings)}")

    if args.delete:
        confirmation = input("\nAre you sure you want to DELETE these duplicate files? (yes/no): ").lower()
        if confirmation == 'yes':
            print("Proceeding with deletion...")
            for file_hash, paths in duplicates.items():
                # Keep the first file, delete the rest
                for path_to_delete in paths[1:]:
                    try:
                        file_size = os.path.getsize(path_to_delete)
                        os.remove(path_to_delete)
                        print(f"  Deleted: {path_to_delete}")
                        deleted_count += 1
                        deleted_size += file_size
                    except (OSError, FileNotFoundError) as e:
                        print(f"  Error deleting {path_to_delete}: {e}", file=sys.stderr)
            print(f"\nDeletion complete. Removed {deleted_count} files, saving {format_bytes(deleted_size)}.")
            sys.exit(0)
        else:
            print("Deletion cancelled.")
            sys.exit(2) # No-op, nothing changed
    else:
        print("\nThis was a dry run. No files were deleted. Use --delete to remove duplicates.")
        sys.exit(0)

if __name__ == "__main__":
    main()
