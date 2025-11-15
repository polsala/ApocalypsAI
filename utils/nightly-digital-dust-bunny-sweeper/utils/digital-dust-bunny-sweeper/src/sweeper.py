import os
import sys
import hashlib
import time
from datetime import datetime, timedelta
import argparse

def get_file_hash(filepath, block_size=65536):
    """Generates MD5 hash for a file."""
    # Mock rationale: In tests, this function will be mocked to return a predictable hash
    # without actually reading file content, ensuring determinism and offline execution.
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_dust_bunnies(
    directory,
    max_size_bytes,
    max_age_days,
    find_duplicates_enabled
):
    """
    Scans a directory for large, old, and duplicate files.
    Returns a dictionary with categorized lists of files.
    """
    giant_files = []
    ancient_files = []
    duplicate_files = {} # hash -> [filepath1, filepath2, ...]

    current_time = time.time()
    age_threshold_timestamp = current_time - (max_age_days * 24 * 60 * 60)

    for root, _, files in os.walk(directory):
        # Mock rationale: os.walk will be mocked in tests to provide a controlled
        # file system structure, making tests deterministic.
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                # Mock rationale: os.path.getsize and os.path.getmtime will be mocked
                # to return predictable values for test files, ensuring determinism.
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)

                if file_size > max_size_bytes:
                    giant_files.append({
                        'path': filepath,
                        'size': file_size,
                        'mtime': datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })

                if file_mtime < age_threshold_timestamp:
                    ancient_files.append({
                        'path': filepath,
                        'size': file_size,
                        'mtime': datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })

                if find_duplicates_enabled:
                    file_hash = get_file_hash(filepath)
                    if file_hash not in duplicate_files:
                        duplicate_files[file_hash] = []
                    duplicate_files[file_hash].append(filepath)

            except OSError as e:
                print(f"Warning: Could not access {filepath} - {e}", file=sys.stderr)
                continue

    # Filter out unique files from duplicates
    actual_duplicates = {
        h: paths for h, paths in duplicate_files.items() if len(paths) > 1
    }

    return {
        'giant_files': giant_files,
        'ancient_files': ancient_files,
        'duplicate_files': actual_duplicates
    }

def format_size(size_bytes):
    """Formats bytes into human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / (1024**2):.2f} MB"
    else:
        return f"{size_bytes / (1024**3):.2f} GB"

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: find large, old, and duplicate files."
    )
    parser.add_argument(
        "directory",
        help="The path to the directory you want to sweep."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=104857600, # 100 MB
        help="Report files larger than this size (in bytes). Default: 100MB."
    )
    parser.add_argument(
        "--max-age",
        type=int,
        default=365, # 365 days
        help="Report files older than this many days. Default: 365 days."
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Enable duplicate file detection. This can be CPU-intensive for large directories."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"🧹 Sweeping '{args.directory}' for digital dust bunnies...")
    print(f"   - Max file size for reporting: {format_size(args.max_size)}")
    print(f"   - Max file age for reporting: {args.max_age} days")
    print(f"   - Duplicate detection: {'Enabled' if args.find_duplicates else 'Disabled'}")
    print("-" * 50)

    results = find_dust_bunnies(
        args.directory,
        args.max_size,
        args.max_age,
        args.find_duplicates
    )

    found_any = False

    if results['giant_files']:
        found_any = True
        print("\n--- 🐘 Giant Files (exceeding {}): ---".format(format_size(args.max_size)))
        for f in results['giant_files']:
            print(f"  - {f['path']} ({format_size(f['size'])}, Modified: {f['mtime']})")

    if results['ancient_files']:
        found_any = True
        print("\n--- 🕰️ Ancient Files (older than {} days): ---".format(args.max_age))
        for f in results['ancient_files']:
            print(f"  - {f['path']} ({format_size(f['size'])}, Modified: {f['mtime']})")

    if results['duplicate_files']:
        found_any = True
        print("\n--- 👯 Duplicate Files: ---")
        for file_hash, paths in results['duplicate_files'].items():
            print(f"  - Hash: {file_hash[:8]}...")
            for p in paths:
                # Mock rationale: os.path.getsize will be mocked to return predictable values.
                print(f"    - {p} ({format_size(os.path.getsize(p))})")

    if not found_any:
        print("\n✨ All clear! No significant digital dust bunnies found. Your digital space is sparkling!")
    else:
        print("\n--- Sweep Complete! ---")
        print("Consider reviewing the identified files for potential cleanup.")

if __name__ == "__main__":
    main()
