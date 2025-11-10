import os
import time
import argparse
from datetime import datetime

def find_debris(root_path, max_age_days=None, include_empty=False, min_size_bytes=0):
    """
    Scans a directory for 'digital debris' based on age, emptiness, and minimum size.

    Args:
        root_path (str): The path to the directory to scan.
        max_age_days (int, optional): Files not accessed in at least this many days are considered debris.
                                      If None, age is not a primary filter unless --empty is also not set.
        include_empty (bool): If True, empty files and directories are considered debris.
        min_size_bytes (int): Only files larger than or equal to this size are considered debris.

    Returns:
        list: A list of dictionaries, each representing a piece of debris.
              Each dict contains 'path', 'type', 'size' (for files), and 'last_access' (for files).
    """
    debris_list = []
    current_time = time.time()

    if not os.path.exists(root_path):
        print(f"Error: Path '{root_path}' does not exist.")
        return []
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a directory.")
        return []

    # Default age if no specific filters are given
    if max_age_days is None and not include_empty:
        max_age_days = 30 # Default to 30 days if no other criteria specified

    age_threshold_timestamp = current_time - (max_age_days * 24 * 3600) if max_age_days is not None else 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check files
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                stat = os.stat(file_path)
                file_size = stat.st_size
                last_access_time = stat.st_atime

                is_old = max_age_days is not None and last_access_time < age_threshold_timestamp
                is_empty_file = include_empty and file_size == 0
                is_large_enough = file_size >= min_size_bytes

                if (is_old or is_empty_file) and is_large_enough:
                    debris_list.append({
                        'path': file_path,
                        'type': 'file',
                        'size': file_size,
                        'last_access': datetime.fromtimestamp(last_access_time).strftime('%Y-%m-%d %H:%M:%S')
                    })
            except OSError as e:
                # Handle permission errors or deleted files during walk
                # print(f"Warning: Could not access '{file_path}': {e}") # Suppress for cleaner output
                continue

        # Check directories for emptiness if requested
        if include_empty:
            try:
                # A directory is empty if os.listdir returns an empty list
                if not os.listdir(dirpath):
                    debris_list.append({
                        'path': dirpath,
                        'type': 'directory',
                        'size': 0,
                        'last_access': None
                    })
            except OSError as e:
                # print(f"Warning: Could not list directory '{dirpath}': {e}") # Suppress for cleaner output
                continue

    return debris_list

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for 'digital debris' (old, unused, or empty files/folders)."
    )
    parser.add_argument(
        'path', 
        type=str, 
        help='The root directory to scan for debris.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        help='Report files not accessed in at least this many days.'
    )
    parser.add_argument(
        '--empty', 
        action='store_true', 
        help='Report empty files and directories.'
    )
    parser.add_argument(
        '--min-size', 
        type=int, 
        default=0, 
        help='Only report files larger than or equal to this size (in bytes).'
    )

    args = parser.parse_args()

    # If no specific filters are provided, default to --age 30
    if args.age is None and not args.empty:
        print("No specific filters provided. Defaulting to --age 30 days.")
        args.age = 30

    debris = find_debris(
        args.path,
        max_age_days=args.age,
        include_empty=args.empty,
        min_size_bytes=args.min_size
    )

    if debris:
        print("\n--- Digital Debris Found ---")
        for item in debris:
            if item['type'] == 'file':
                size_str = f" ({item['size']} bytes)" if item['size'] > 0 else " (empty)"
                access_str = f" (last accessed: {item['last_access']})" if item['last_access'] else ""
                print(f"[FILE] {item['path']}{size_str}{access_str}")
            elif item['type'] == 'directory':
                print(f"[DIR] {item['path']} (empty)")
    else:
        print("\nNo digital debris found. Your data bunker is pristine!")

if __name__ == '__main__':
    main()
