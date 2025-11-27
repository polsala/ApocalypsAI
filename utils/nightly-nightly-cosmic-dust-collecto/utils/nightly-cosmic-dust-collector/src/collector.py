import os
import time
import argparse
from datetime import datetime

def find_cosmic_dust(
    directory: str,
    max_size_bytes: int = 1024,  # Default to 1KB
    max_age_days: int = 90,      # Default to 90 days
) -> list[dict]:
    """
    Scans a directory for files considered 'cosmic dust'.

    Args:
        directory: The path to the directory to scan.
        max_size_bytes: Files smaller than this (in bytes) are considered small.
        max_age_days: Files older than this (in days) are considered old.

    Returns:
        A list of dictionaries, each representing a 'dust' file with its properties.
    """
    dust_files = []
    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60

    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                file_size = stat.st_size
                last_modified_time = stat.st_mtime

                is_empty = file_size == 0
                # A file is 'small' if its size is greater than 0 but less than max_size_bytes
                is_small = file_size > 0 and file_size < max_size_bytes
                is_old = (current_time - last_modified_time) > max_age_seconds

                if is_empty or is_small or is_old:
                    reasons = []
                    if is_empty: reasons.append('empty')
                    if is_small: reasons.append('small')
                    if is_old: reasons.append('old')

                    dust_files.append({
                        'path': filepath,
                        'size_bytes': file_size,
                        'last_modified': datetime.fromtimestamp(last_modified_time).isoformat(),
                        'reasons': reasons
                    })
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.stat
                continue
            except Exception as e:
                print(f"Warning: Could not process {filepath}: {e}")
                continue

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for 'cosmic dust' files (empty, small, or old)."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024,
        help="Maximum file size in bytes to consider a file 'small'. Default: 1024 (1KB)."
    )
    parser.add_argument(
        "--max-age",
        type=int,
        default=90,
        help="Maximum age in days (since last modification) to consider a file 'old'. Default: 90 days."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for cosmic dust...")
    print(f"  Max size for 'small': {args.max_size} bytes")
    print(f"  Max age for 'old': {args.max_age} days")

    dust = find_cosmic_dust(args.directory, args.max_size, args.max_age)

    if dust:
        print(f"\nFound {len(dust)} cosmic dust files:")
        for item in dust:
            reasons = ', '.join(item['reasons'])
            print(f"- {item['path']} (Size: {item['size_bytes']} bytes, Modified: {item['last_modified']}, Reasons: {reasons})")
    else:
        print("\nNo cosmic dust found. Your repository is sparkling clean!")

if __name__ == "__main__":
    main()
