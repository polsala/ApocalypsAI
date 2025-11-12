import os
import time
import argparse
from datetime import datetime

def find_dust_bunnies(root_dir, age_days, max_size_bytes):
    """
    Scans a directory for files older than 'age_days' and smaller than 'max_size_bytes'.
    Returns a list of dictionaries, each representing a 'dust bunny' file.
    """
    dust_bunnies = []
    current_time = time.time()
    age_seconds = age_days * 24 * 60 * 60

    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}")
        return []

    # print(f"Scanning {root_dir} for cosmic dust bunnies...") # Commented for cleaner test output

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Ensure it's a regular file before checking its properties
                if not os.path.isfile(file_path):
                    continue

                file_mtime = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)

                if (current_time - file_mtime) > age_seconds and file_size < max_size_bytes:
                    dust_bunnies.append({
                        'path': file_path,
                        'size': file_size,
                        'mtime': file_mtime
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                # print(f"Warning: Could not access {file_path}: {e}") # Commented for cleaner test output
                continue
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Finds small, old files ('cosmic dust bunnies') in a directory."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start scanning from.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        default=30, 
        help='Files older than this many days will be considered old. Default: 30.'
    )
    parser.add_argument(
        '--max-size', 
        type=int, 
        default=1048576, # 1 MB
        help='Files larger than this size (in bytes) will be ignored. Default: 1048576 (1 MB).'
    )

    args = parser.parse_args()

    print(f"Scanning {args.path} for cosmic dust bunnies...")
    dust_bunnies = find_dust_bunnies(args.path, args.age, args.max_size)

    if dust_bunnies:
        print(f"\nFound {len(dust_bunnies)} cosmic dust bunnies:\n")
        for bunny in dust_bunnies:
            mtime_dt = datetime.fromtimestamp(bunny['mtime'])
            age_in_days = (time.time() - bunny['mtime']) / (24 * 60 * 60)
            print(f"- Path: {bunny['path']}")
            print(f"  Size: {bunny['size']} bytes")
            print(f"  Last Modified: {mtime_dt.strftime('%Y-%m-%d %H:%M:%S')} ({int(age_in_days)} days ago)")
        print("\nCleanup suggestions:\nConsider archiving or deleting these files to free up space and declutter your project.")
    else:
        print("\nNo cosmic dust bunnies found. Your directory is sparkling clean!")

if __name__ == '__main__':
    main()
