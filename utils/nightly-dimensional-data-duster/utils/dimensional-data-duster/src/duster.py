import os
import hashlib
import argparse
import sys

CHUNK_SIZE = 65536  # 64KB

def calculate_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(directories, dry_run=True, delete=False):
    """Finds and optionally deletes duplicate files in specified directories."""
    if not directories:
        print("No directories provided to scan.", file=sys.stderr)
        return

    all_files = []
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not accessible: {directory}", file=sys.stderr)
            continue
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    all_files.append(filepath)

    if not all_files:
        print("No files found to scan.")
        return

    # Group files by size first for efficiency
    files_by_size = {}
    for filepath in all_files:
        try:
            size = os.path.getsize(filepath)
            files_by_size.setdefault(size, []).append(filepath)
        except OSError as e:
            print(f"Warning: Could not get size for {filepath}: {e}", file=sys.stderr)

    # Now group by hash for files with identical sizes
    duplicate_groups = []
    for size, filepaths in files_by_size.items():
        if len(filepaths) > 1: # Only check for duplicates if there's more than one file of this size
            files_by_hash = {}
            for filepath in filepaths:
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    files_by_hash.setdefault(file_hash, []).append(filepath)
            
            for file_hash, hash_group in files_by_hash.items():
                if len(hash_group) > 1:
                    duplicate_groups.append(hash_group)

    if not duplicate_groups:
        print("No duplicate files found. Your dimensions are pristine!")
        return

    print(f"Found {len(duplicate_groups)} groups of duplicate files:")
    total_saved_size = 0

    for group_idx, group in enumerate(duplicate_groups):
        print(f"\n--- Duplicate Group {group_idx + 1} ---")
        original_file = group[0]
        print(f"  Keeping: {original_file}")
        
        # Calculate potential savings if duplicates were removed
        try:
            file_size = os.path.getsize(original_file)
            saved_size_for_group = file_size * (len(group) - 1)
            total_saved_size += saved_size_for_group
        except OSError as e:
            print(f"Warning: Could not get size for {original_file}: {e}", file=sys.stderr)
            saved_size_for_group = 0

        for i in range(1, len(group)):
            duplicate_file = group[i]
            if delete and not dry_run:
                try:
                    os.remove(duplicate_file)
                    print(f"  Deleted: {duplicate_file}")
                except OSError as e:
                    print(f"  Error deleting {duplicate_file}: {e}", file=sys.stderr)
            else:
                print(f"  Duplicate (would delete): {duplicate_file}")
    
    if dry_run or not delete:
        print(f"\nTotal potential space saved by removing duplicates: {total_saved_size / (1024*1024):.2f} MB")
        print("Run with --delete to remove these files.")
    else:
        print(f"\nTotal space saved: {total_saved_size / (1024*1024):.2f} MB")
        print("Duplicate files have been removed.")

def main():
    parser = argparse.ArgumentParser(
        description="Dimensional Data Duster: Find and optionally delete duplicate files."
    )
    parser.add_argument(
        'directories', 
        metavar='directory', 
        type=str, 
        nargs='+',
        help='One or more directories to scan for duplicate files.'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Perform a scan and report duplicates without deleting any files (default).'
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='Delete duplicate files, keeping one instance of each unique file. Use with caution!'
    )

    args = parser.parse_args()

    if args.delete:
        # If --delete is specified, it overrides --dry-run
        find_duplicate_files(args.directories, dry_run=False, delete=True)
    else:
        # Default to dry-run if --delete is not specified
        find_duplicate_files(args.directories, dry_run=True, delete=False)

if __name__ == '__main__':
    main()
