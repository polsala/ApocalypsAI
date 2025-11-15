import os
import sys
import time
import argparse
from datetime import datetime, timedelta

def get_file_info(filepath):
    """Returns a dictionary with file path, size, and last modification timestamp."""
    try:
        stat = os.stat(filepath)
        return {
            'path': filepath,
            'size': stat.st_size,
            'mtime': stat.st_mtime
        }
    except OSError:
        return None

def format_size(bytes_size):
    """Formats bytes into human-readable string (KB, MB, GB)."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024**2:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024**3:
        return f"{bytes_size / (1024**2):.1f} MB"
    else:
        return f"{bytes_size / (1024**3):.1f} GB"

def scan_directory(directory_path, min_size_mb=100, min_age_days=365):
    """
    Scans a directory for large files and old files.

    Args:
        directory_path (str): The path to the directory to scan.
        min_size_mb (int): Minimum size in MB for a file to be considered "large".
        min_age_days (int): Minimum age in days for a file to be considered "old".

    Returns:
        tuple: (list of large files, list of old files)
    """
    large_files = []
    old_files = []

    min_size_bytes = min_size_mb * (1024**2)
    cutoff_time = time.time() - (min_age_days * 24 * 60 * 60)

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'", file=sys.stderr)
        return [], []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_info = get_file_info(filepath)

            if file_info:
                if file_info['size'] >= min_size_bytes:
                    large_files.append(file_info)
                if file_info['mtime'] <= cutoff_time:
                    old_files.append(file_info)
    return large_files, old_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for 'digital dust bunnies' (large or old files)."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory you want to scan."
    )
    parser.add_argument(
        "--min-size-mb",
        type=int,
        default=100,
        help="Report files larger than this size in megabytes. Default: 100 MB."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=365,
        help="Report files whose last modification date is older than this many days. Default: 365 days."
    )

    args = parser.parse_args()

    print(f"Scanning directory: {args.directory_path}")
    print(f"Thresholds: Min Size = {args.min_size_mb:.1f} MB, Min Age = {args.min_age_days} days")
    print("\n--- Digital Dust Bunnies Report ---\n")

    large_files, old_files = scan_directory(
        args.directory_path, args.min_size_mb, args.min_age_days
    )

    found_any = False

    if large_files:
        found_any = True
        print(f"Large Files (>= {args.min_size_mb:.1f} MB):")
        for f in sorted(large_files, key=lambda x: x['size'], reverse=True):
            mod_date = datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d')
            print(f"- {f['path']} (Size: {format_size(f['size'])}, Modified: {mod_date})")
        print()

    if old_files:
        found_any = True
        print(f"Ancient Files (Modified >= {args.min_age_days} days ago):")
        for f in sorted(old_files, key=lambda x: x['mtime']):
            mod_date = datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d')
            print(f"- {f['path']} (Size: {format_size(f['size'])}, Modified: {mod_date})")
        print()

    if not found_any:
        print("No dust bunnies found matching criteria.")

if __name__ == "__main__":
    main()
