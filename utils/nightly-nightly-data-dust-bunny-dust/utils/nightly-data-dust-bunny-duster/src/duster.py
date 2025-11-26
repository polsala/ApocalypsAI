import os
import hashlib
import shutil
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

def get_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_stale_files(directory, stale_days):
    """Finds files not modified within the last `stale_days`."""
    if stale_days <= 0:
        return []

    stale_threshold = datetime.now() - timedelta(days=stale_days)
    stale_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Use mtime (modification time) as it's more reliable than atime
                # which can be affected by system settings or disabled.
                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)
                if mod_datetime < stale_threshold:
                    stale_files.append((filepath, mod_datetime.strftime('%Y-%m-%d')))
            except OSError:
                # Handle cases where file might be inaccessible or deleted during scan
                continue
    return stale_files

def find_duplicate_files(directory):
    """Finds duplicate files based on size and then MD5 hash."""
    files_by_size = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                files_by_size[size].append(filepath)
            except OSError:
                continue

    duplicate_groups = defaultdict(list)
    for size, file_list in files_by_size.items():
        if size == 0: # Skip empty files, they are technically duplicates but often not useful to report
            continue
        if len(file_list) > 1:
            files_by_hash = defaultdict(list)
            for filepath in file_list:
                try:
                    file_hash = get_file_hash(filepath)
                    files_by_hash[file_hash].append(filepath)
                except OSError:
                    continue
            for file_hash, duplicates in files_by_hash.items():
                if len(duplicates) > 1:
                    duplicate_groups[file_hash].extend(duplicates)
    return duplicate_groups

def quarantine_files(file_paths, quarantine_dir):
    """Moves files to a quarantine directory, handling name conflicts."""
    os.makedirs(quarantine_dir, exist_ok=True)
    quarantined_count = 0
    for filepath in file_paths:
        filename = os.path.basename(filepath)
        dest_path = os.path.join(quarantine_dir, filename)
        counter = 1
        while os.path.exists(dest_path):
            name_parts = os.path.splitext(filename)
            dest_path = os.path.join(quarantine_dir, f"{name_parts[0]}_{counter}{name_parts[1]}")
            counter += 1
        try:
            shutil.move(filepath, dest_path)
            quarantined_count += 1
            print(f"  Moved: {filepath} -> {dest_path}")
        except OSError as e:
            print(f"  Error moving {filepath}: {e}")
    return quarantined_count

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Dust Bunny Duster: Find and quarantine stale or duplicate files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan."
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=0,
        help="Files not modified in N days are considered stale. Set to 0 to disable. (Default: 0)"
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="If present, the utility will search for duplicate files."
    )
    parser.add_argument(
        "--quarantine-dir",
        type=str,
        help="Path to a directory where identified files will be moved. If not provided, files are only reported."
    )

    args = parser.parse_args()

    print(f"Scanning {args.directory}...")

    all_files_to_quarantine = []
    stale_files_report = []
    duplicate_files_report = {}

    # Find stale files
    if args.stale_days > 0:
        stale_files_report = find_stale_files(args.directory, args.stale_days)
        if stale_files_report:
            print(f"\n--- Stale Files (not modified in {args.stale_days} days) ---")
            for filepath, mod_date in stale_files_report:
                print(f"  - {filepath} (Last modified: {mod_date})")
                all_files_to_quarantine.append(filepath)
        else:
            print(f"\n--- Stale Files (not modified in {args.stale_days} days) ---
  No stale files found.")

    # Find duplicate files
    if args.find_duplicates:
        duplicate_files_report = find_duplicate_files(args.directory)
        if duplicate_files_report:
            print("\n--- Duplicate Files ---")
            for file_hash, duplicates in duplicate_files_report.items():
                print(f"  - Hash: {file_hash[:10]}...")
                # Add all but one duplicate to quarantine list
                for i, filepath in enumerate(duplicates):
                    print(f"    - {filepath}")
                    if i > 0: # Keep the first instance, quarantine the rest
                        all_files_to_quarantine.append(filepath)
        else:
            print("\n--- Duplicate Files ---
  No duplicate files found.")

    print("\n--- Summary ---")
    print(f"Found {len(stale_files_report)} stale files.")
    total_duplicates = sum(len(v) for v in duplicate_files_report.values())
    print(f"Found {len(duplicate_files_report)} groups of duplicate files ({total_duplicates} files total).")

    quarantined_count = 0
    if args.quarantine_dir and all_files_to_quarantine:
        print(f"\n--- Quarantining Files to {args.quarantine_dir} ---")
        quarantined_count = quarantine_files(list(set(all_files_to_quarantine)), args.quarantine_dir) # Use set to avoid moving same file twice
        print(f"Quarantined {quarantined_count} files.")
    elif args.quarantine_dir and not all_files_to_quarantine:
        print("No files to quarantine.")
    else:
        print("No files were quarantined (use --quarantine-dir to enable).")

    if not stale_files_report and not duplicate_files_report:
        print("No issues found. Your digital space is sparkling clean!")

if __name__ == "__main__":
    main()
