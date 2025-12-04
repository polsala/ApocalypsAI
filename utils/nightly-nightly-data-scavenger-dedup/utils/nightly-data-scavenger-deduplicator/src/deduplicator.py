import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    if not os.path.isfile(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """
    Scans a directory for duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    hashes = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)
    
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def remove_duplicate_files(duplicates_map, dry_run=True):
    """
    Removes duplicate files, keeping one original for each set of duplicates.
    Returns a list of files that would be/were removed.
    """
    removed_files = []
    for file_hash, paths in duplicates_map.items():
        if len(paths) > 1:
            # Keep the first file, remove the rest
            files_to_remove = paths[1:]
            for filepath in files_to_remove:
                if not dry_run:
                    try:
                        os.remove(filepath)
                        removed_files.append(filepath)
                    except OSError as e:
                        print(f"Error removing {filepath}: {e}")
                else:
                    removed_files.append(filepath) # For dry run, just list them
    return removed_files

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Data Scavenger & De-Duplicator: Scans directories for duplicate files and optionally removes them."
    )
    parser.add_argument(
        "directories",
        nargs=":",
        help="One or more directories to scan for duplicate files."
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Actually remove duplicate files. By default, it's a dry run."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output of files found and removed."
    )

    args = parser.parse_args()

    if not args.directories:
        print("Error: No directories provided. Please specify one or more directories to scan.")
        parser.print_help()
        return

    all_duplicates = {}
    for directory in args.directories:
        try:
            print(f"Scanning '{directory}' for duplicates...")
            duplicates_in_dir = find_duplicate_files(directory)
            if duplicates_in_dir:
                all_duplicates.update(duplicates_in_dir)
            else:
                print(f"No duplicates found in '{directory}'.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

    if not all_duplicates:
        print("No duplicate files found across all scanned directories.")
        return

    print("\n--- Duplicate Files Report ---")
    total_duplicates_found = 0
    for file_hash, paths in all_duplicates.items():
        if len(paths) > 1:
            total_duplicates_found += (len(paths) - 1)
            if args.verbose:
                print(f"Hash: {file_hash}")
                print(f"  Original: {paths[0]}")
                for p in paths[1:]:
                    print(f"  Duplicate: {p}")
                print("-" * 20)

    print(f"\nTotal unique sets of duplicates: {len(all_duplicates)}")
    print(f"Total duplicate files (excluding originals) found: {total_duplicates_found}")

    if total_duplicates_found > 0:
        if args.remove:
            print("\n--- Removing Duplicates (Live Run) ---")
            removed_files = remove_duplicate_files(all_duplicates, dry_run=False)
            print(f"Successfully removed {len(removed_files)} duplicate files.")
            if args.verbose and removed_files:
                print("Removed files:")
                for f in removed_files:
                    print(f"  - {f}")
        else:
            print("\n--- Dry Run: Duplicates would be removed with --remove ---")
            removed_files_dry_run = remove_duplicate_files(all_duplicates, dry_run=True)
            print(f"Would remove {len(removed_files_dry_run)} duplicate files.")
            if args.verbose and removed_files_dry_run:
                print("Files that would be removed:")
                for f in removed_files_dry_run:
                    print(f"  - {f}")
    else:
        print("No files to remove.")

if __name__ == "__main__":
    main()
