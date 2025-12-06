import os
import time
import argparse
from datetime import datetime

def get_file_stats(filepath):
    """Returns (access_time_timestamp, modification_time_timestamp, size_bytes)."""
    try:
        stat = os.stat(filepath)
        return stat.st_atime, stat.st_mtime, stat.st_size
    except OSError:
        return None, None, None

def is_file_old(filepath, days_threshold, current_time_timestamp):
    """Checks if a file hasn't been accessed or modified within the threshold.
    Returns (is_accessed_old, is_modified_old)."""
    atime, mtime, _ = get_file_stats(filepath)
    if atime is None or mtime is None:
        return False, False # Cannot get stats, assume not old

    # Convert seconds to days
    accessed_days_ago = (current_time_timestamp - atime) / (24 * 3600)
    modified_days_ago = (current_time_timestamp - mtime) / (24 * 3600)

    is_accessed_old = accessed_days_ago > days_threshold
    is_modified_old = modified_days_ago > days_threshold
    return is_accessed_old, is_modified_old

def is_file_empty(filepath):
    """Checks if a file is empty."""
    _, _, size = get_file_stats(filepath)
    return size == 0 if size is not None else False

def collect_debris(directory, days_threshold):
    """Scans a directory for old and empty files."""
    current_time_timestamp = time.time()
    old_files = []
    empty_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Check for old files
            is_accessed_old, is_modified_old = is_file_old(filepath, days_threshold, current_time_timestamp)
            if is_accessed_old or is_modified_old:
                atime, mtime, _ = get_file_stats(filepath) # Re-get stats for reporting
                old_files.append({
                    'path': filepath,
                    'accessed_old': is_accessed_old,
                    'modified_old': is_modified_old,
                    'atime': datetime.fromtimestamp(atime).isoformat() if atime else 'N/A',
                    'mtime': datetime.fromtimestamp(mtime).isoformat() if mtime else 'N/A',
                })

            # Check for empty files
            if is_file_empty(filepath):
                empty_files.append({'path': filepath})
    
    return old_files, empty_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for digital debris (old and empty files)."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for debris."
    )
    parser.add_argument(
        "--days-threshold",
        type=int,
        default=90,
        help="Files not accessed or modified in this many days are considered 'old'. Default is 90."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        exit(1)

    print(f"Scanning '{args.directory}' for digital debris (threshold: {args.days_threshold} days)...")
    old_files, empty_files = collect_debris(args.directory, args.days_threshold)

    if not old_files and not empty_files:
        print("\n✨ Your digital bunker is sparkling clean! No debris found. ✨")
    else:
        print("\n--- Digital Debris Report ---")
        if old_files:
            print(f"\nFound {len(old_files)} 'old' files (not accessed/modified in {args.days_threshold} days):")
            for file_info in old_files:
                status = []
                if file_info['accessed_old']:
                    status.append(f"Accessed: {file_info['atime']}")
                if file_info['modified_old']:
                    status.append(f"Modified: {file_info['mtime']}")
                print(f"  - {file_info['path']} ({'; '.join(status)})")
        
        if empty_files:
            print(f"\nFound {len(empty_files)} 'empty' files:")
            for file_info in empty_files:
                print(f"  - {file_info['path']}")
        
        print("\nConsider reviewing these files for potential cleanup.")

if __name__ == "__main__":
    main()
