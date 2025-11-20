import os
import time
import argparse
from datetime import datetime

def find_empty_directories(root_path):
    """Recursively finds all truly empty directories within a given root path.
    A directory is considered truly empty if it contains no files and no subdirectories.
    """
    truly_empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if not dirnames and not filenames:
            truly_empty_dirs.append(dirpath)
    return truly_empty_dirs

def find_stale_files(root_path, age_days, max_size_mb):
    """Recursively finds files older than age_days and smaller than max_size_mb."""
    stale_files = []
    cutoff_time = time.time() - (age_days * 24 * 60 * 60) # seconds since epoch
    max_size_bytes = max_size_mb * 1024 * 1024 # MB to bytes

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Skip if it's not a regular file (e.g., symlinks, broken links, directories)
                if not os.path.isfile(filepath):
                    continue

                mod_time = os.path.getmtime(filepath)
                file_size = os.path.getsize(filepath)

                if mod_time < cutoff_time and file_size < max_size_bytes:
                    stale_files.append({
                        'path': filepath,
                        'modified': datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S'),
                        'size_mb': round(file_size / (1024 * 1024), 2)
                    })
            except (OSError, FileNotFoundError): # Handle permission errors or files disappearing during scan
                pass
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Identify digital 'dust bunnies' (empty directories and stale files).
        This tool only reports and does not delete anything."
    )
    parser.add_argument(
        '--path', type=str, default='.',
        help='The root directory to start scanning from. Defaults to current directory.'
    )
    parser.add_argument(
        '--age-days', type=int, default=30,
        help='Files older than this many days will be considered stale. Defaults to 30.'
    )
    parser.add_argument(
        '--max-size-mb', type=int, default=1,
        help='Files smaller than this many megabytes will be considered stale. Defaults to 1.'
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    age_days = args.age_days
    max_size_mb = args.max_size_mb

    print(f"Scanning {root_path} for digital dust bunnies...")

    empty_dirs = find_empty_directories(root_path)
    stale_files = find_stale_files(root_path, age_days, max_size_mb)

    print("\n🧹 Found {} Empty Directories:".format(len(empty_dirs)))
    if empty_dirs:
        for d in empty_dirs:
            print(f"  - {d}")
    else:
        print("  None found. Your directories are sparkling clean!")

    print(f"\n⏳ Found {len(stale_files)} Stale Files (older than {age_days} days, smaller than {max_size_mb}MB):")
    if stale_files:
        for f in stale_files:
            print(f"  - {f['path']} (Modified: {f['modified']}, Size: {f['size_mb']:.2f} MB)")
    else:
        print("  None found. Your files are fresh and vital!")

    print("\nScan complete. Time to get sweeping!")

if __name__ == '__main__':
    main()
