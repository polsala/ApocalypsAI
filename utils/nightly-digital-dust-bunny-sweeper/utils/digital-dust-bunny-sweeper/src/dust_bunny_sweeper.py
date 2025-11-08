import os
import hashlib
import time
import argparse
from collections import defaultdict

def get_file_hash(filepath, block_size=65536):
    """Generates a SHA256 hash for a given file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_digital_dust_bunnies(directory, age_threshold_days=365, min_size_bytes=0):
    """Scans a directory for old and duplicate files (digital dust bunnies)."""
    current_time = time.time()
    old_files = []
    hashes = defaultdict(list)
    total_scanned_size = 0
    total_scanned_files = 0

    print(f"\n--- Sweeping '{directory}' for Digital Dust Bunnies ---")
    print(f"  Age threshold: {age_threshold_days} days")
    print(f"  Minimum file size: {min_size_bytes} bytes\n")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                try:
                    file_stat = os.stat(filepath)
                    file_size = file_stat.st_size
                    file_mtime = file_stat.st_mtime

                    if file_size < min_size_bytes:
                        continue # Skip files smaller than min_size

                    total_scanned_files += 1
                    total_scanned_size += file_size

                    # Check for old files
                    if (current_time - file_mtime) / (24 * 3600) > age_threshold_days:
                        old_files.append((filepath, file_size, file_mtime))

                    # Check for duplicates (only if file is not too small)
                    file_hash = get_file_hash(filepath)
                    hashes[file_hash].append((filepath, file_size))

                except OSError as e:
                    print(f"Warning: Could not access '{filepath}': {e}")
                except Exception as e:
                    print(f"Error processing '{filepath}': {e}")

    duplicate_groups = {h: files for h, files in hashes.items() if len(files) > 1}

    print(f"--- Sweep Complete ---")
    print(f"Scanned {total_scanned_files} files, total size: {total_scanned_size / (1024*1024):.2f} MB\n")

    if old_files:
        print("### Fluffy Dust Bunnies (Old Files) ###")
        print(f"Found {len(old_files)} files older than {age_threshold_days} days:")
        for path, size, mtime in sorted(old_files, key=lambda x: x[2]):
            print(f"  - {path} ({(current_time - mtime) / (24 * 3600):.0f} days old, {size / 1024:.2f} KB)")
        print()

    if duplicate_groups:
        print("### Tangled Dust Clumps (Duplicate Files) ###")
        print(f"Found {len(duplicate_groups)} groups of duplicate files:")
        for h, files in duplicate_groups.items():
            total_duplicate_size = sum(f[1] for f in files)
            print(f"  - Hash: {h[:8]}... (Total size: {total_duplicate_size / 1024:.2f} KB, {len(files)} copies)")
            for path, size in files:
                print(f"    - {path} ({size / 1024:.2f} KB)")
        print()

    if not old_files and not duplicate_groups:
        print("✨ Your digital space is sparkling clean! No dust bunnies found. ✨\n")

    return old_files, duplicate_groups


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Sweep your digital space for old and duplicate files (digital dust bunnies)."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=365,
        help="Files older than this many days will be flagged as 'fluffy dust bunnies'. Default: 365."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=0,
        help="Only consider files larger than this size (in bytes) for scanning. Default: 0."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found or is not a directory.")
        exit(1)

    find_digital_dust_bunnies(args.directory, args.age_days, args.min_size)
