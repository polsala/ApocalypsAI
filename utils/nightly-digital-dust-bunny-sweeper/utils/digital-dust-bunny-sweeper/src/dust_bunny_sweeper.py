import os
import time
import argparse
from datetime import datetime, timedelta

def find_dust_bunnies(
    scan_path: str,
    older_than_days: int = 365,
    larger_than_bytes: int = 1048576
) -> list[dict]:
    """
    Scans the specified path for files older than 'older_than_days' and
    larger than 'larger_than_bytes'.

    Args:
        scan_path: The root directory to start scanning from.
        older_than_days: Files older than this many days will be considered.
        larger_than_bytes: Files larger than this many bytes will be considered.

    Returns:
        A list of dictionaries, each representing a "dust bunny" file with
        'path', 'age_days', and 'size_bytes'.
    """
    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.")
        return []

    dust_bunnies = []
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(days=older_than_days)

    print(f"Scanning '{scan_path}' for digital dust bunnies...")
    print(f"  - Older than: {older_than_days} days")
    print(f"  - Larger than: {larger_than_bytes / (1024 * 1024):.2f} MB")
    print("-" * 40)

    for root, _, files in os.walk(scan_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                file_stat = os.stat(file_path)
                file_mod_time = datetime.fromtimestamp(file_stat.st_mtime)
                file_size = file_stat.st_size

                if file_mod_time < cutoff_time and file_size > larger_than_bytes:
                    age_days = (current_time - file_mod_time).days
                    dust_bunnies.append({
                        "path": file_path,
                        "age_days": age_days,
                        "size_bytes": file_size
                    })
            except OSError as e:
                # Handle cases where file might be deleted or permissions issue
                print(f"Warning: Could not access '{file_path}': {e}")
                continue
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify digital dust bunnies (old and large files) for decluttering."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for digital dust bunnies."
    )
    parser.add_argument(
        "--older-than-days",
        type=int,
        default=365,
        help="Only show files older than this many days. Default: 365."
    )
    parser.add_argument(
        "--larger-than-bytes",
        type=int,
        default=1048576,  # 1 MB
        help="Only show files larger than this many bytes. Default: 1048576 (1MB)."
    )

    args = parser.parse_args()

    bunnies = find_dust_bunnies(
        args.path,
        args.older_than_days,
        args.larger_than_bytes
    )

    if bunnies:
        print("\nFound these digital dust bunnies (suggested for removal):")
        for bunny in bunnies:
            size_mb = bunny['size_bytes'] / (1024 * 1024)
            print(f"  - Path: {bunny['path']}")
            print(f"    Age: {bunny['age_days']} days, Size: {size_mb:.2f} MB")
            print("-" * 20)
        print(f"\nTotal dust bunnies found: {len(bunnies)}")
        print("Note: This utility only suggests files; it does not delete anything.")
    else:
        print("\nNo digital dust bunnies found matching your criteria. Your digital space is sparkling clean!")

if __name__ == "__main__":
    main()
