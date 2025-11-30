import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo=hashlib.sha256, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hash_algo()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # File might be inaccessible or not exist

def find_duplicate_files(directory):
    """
    Scans a directory for duplicate files based on content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    files_by_size = defaultdict(list)
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid issues
                continue
            try:
                size = os.path.getsize(filepath)
                if size > 0: # Only consider non-empty files
                    files_by_size[size].append(filepath)
            except OSError:
                # File might be inaccessible, skip it
                continue

    files_by_hash = defaultdict(list)
    for size, filepaths in files_by_size.items():
        if len(filepaths) < 2: # No duplicates possible for this size
            continue
        for filepath in filepaths:
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                files_by_hash[file_hash].append(filepath)

    # Filter out hashes that only have one file (not duplicates)
    duplicate_groups = {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}
    return duplicate_groups

def link_duplicates(duplicate_groups, dry_run=True):
    """
    Replaces duplicate files with hard links to the first encountered file in each group.
    """
    actions = []
    for file_hash, filepaths in duplicate_groups.items():
        if not filepaths:
            continue

        # The first file in the list will be the "original"
        original_file = filepaths[0]
        
        # Ensure the original file still exists before linking
        if not os.path.exists(original_file):
            actions.append(f"WARNING: Original file '{original_file}' for hash {file_hash[:8]}... not found. Skipping group.")
            continue

        for i in range(1, len(filepaths)):
            duplicate_file = filepaths[i]
            if os.path.exists(duplicate_file) and not os.path.samefile(original_file, duplicate_file):
                if dry_run:
                    actions.append(f"DRY RUN: Would replace '{duplicate_file}' with hard link to '{original_file}'")
                else:
                    try:
                        os.remove(duplicate_file)
                        os.link(original_file, duplicate_file)
                        actions.append(f"LINKED: '{duplicate_file}' now links to '{original_file}'")
                    except OSError as e:
                        actions.append(f"ERROR: Could not link '{duplicate_file}' to '{original_file}': {e}")
            elif os.path.exists(duplicate_file) and os.path.samefile(original_file, duplicate_file):
                actions.append(f"SKIPPED: '{duplicate_file}' is already a hard link to '{original_file}'")
            else:
                actions.append(f"WARNING: Duplicate file '{duplicate_file}' not found. Skipping.")
    return actions

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Nightly Quantum Entanglement Linker: Finds and optionally hard-links duplicate files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("directory", help="The root directory to scan for duplicate files.")
    parser.add_argument(
        "--mode",
        choices=["report", "link-dry-run", "link-execute"],
        default="report",
        help="""Operation mode:
  report:       (Default) List all groups of duplicate files.
  link-dry-run: Show which files would be replaced by hard links.
  link-execute: Replace duplicate files with hard links (DANGER: modifies files!)."""
    )
    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for duplicate files...")
    duplicate_groups = find_duplicate_files(args.directory)

    if not duplicate_groups:
        print("No duplicate files found. The cosmos is in order.")
        sys.exit(0)

    print(f"Found {len(duplicate_groups)} groups of duplicate files.")

    if args.mode == "report":
        for file_hash, filepaths in duplicate_groups.items():
            print(f"\nHash: {file_hash}")
            for filepath in filepaths:
                print(f"  - {filepath}")
    elif args.mode in ["link-dry-run", "link-execute"]:
        dry_run = (args.mode == "link-dry-run")
        print(f"\n{'DRY RUN' if dry_run else 'EXECUTING'} hard-linking operation...")
        actions = link_duplicates(duplicate_groups, dry_run=dry_run)
        for action in actions:
            print(action)
        if not dry_run:
            print("\nHard-linking complete. Verify your file system integrity.")

if __name__ == "__main__":
    main()
