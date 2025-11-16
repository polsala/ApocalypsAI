import os
import hashlib
import argparse
from datetime import datetime, timedelta

def get_file_info(filepath):
    """Retrieves file size, modification time, and content hash."""
    try:
        size = os.path.getsize(filepath)
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        # Calculate MD5 hash for content comparison
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            # Read in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()
        
        return {
            'path': filepath,
            'size': size,
            'mod_time': mod_time,
            'hash': file_hash
        }
    except OSError as e:
        print(f"Warning: Could not get info for {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def find_old_files(files_info, days_old):
    """Finds files older than a specified number of days."""
    if not days_old:
        return []
    
    threshold_date = datetime.now() - timedelta(days=days_old)
    old_files = [f for f in files_info if f['mod_time'] < threshold_date]
    return old_files

def find_large_files(files_info, min_size_mb):
    """Finds files larger than a specified size in MB."""
    if not min_size_mb:
        return []
        
    min_size_bytes = min_size_mb * 1024 * 1024
    large_files = [f for f in files_info if f['size'] > min_size_bytes]
    return large_files

def find_duplicate_files(files_info):
    """Finds files with identical content hashes."""
    duplicates = {}
    for f in files_info:
        duplicates.setdefault(f['hash'], []).append(f)
    
    # Filter out hashes that only appear once
    duplicate_groups = {h: paths for h, paths in duplicates.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Data-Dust Defragmenter: Identify old, large, or duplicate files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The directory to scan for data dust."
    )
    parser.add_argument(
        "--old-days",
        type=int,
        help="Report files older than this many days."
    )
    parser.add_argument(
        "--min-size-mb",
        type=int,
        help="Report files larger than this many megabytes."
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Enable duplicate file detection (can be slow for very large directories)."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        return

    all_files_info = []
    print(f"Scanning '{args.path}' for data dust...")
    for root, _, files in os.walk(args.path):
        for filename in files:
            filepath = os.path.join(root, filename)
            info = get_file_info(filepath)
            if info:
                all_files_info.append(info)

    print("\n--- Data Dust Report ---")

    # Initialize lists to ensure they exist for the final check
    old_files = []
    large_files = []
    duplicate_groups = {}

    # Old Files
    if args.old_days:
        old_files = find_old_files(all_files_info, args.old_days)
        if old_files:
            print(f"\nFound {len(old_files)} files older than {args.old_days} days:")
            for f in old_files:
                print(f"  - {f['path']} (Modified: {f['mod_time'].strftime('%Y-%m-%d')})")
        else:
            print(f"\nNo files found older than {args.old_days} days.")

    # Large Files
    if args.min_size_mb:
        large_files = find_large_files(all_files_info, args.min_size_mb)
        if large_files:
            print(f"\nFound {len(large_files)} files larger than {args.min_size_mb} MB:")
            for f in large_files:
                print(f"  - {f['path']} ({f['size'] / (1024*1024):.2f} MB)")
        else:
            print(f"\nNo files found larger than {args.min_size_mb} MB.")

    # Duplicate Files
    if args.find_duplicates:
        duplicate_groups = find_duplicate_files(all_files_info)
        if duplicate_groups:
            print(f"\nFound {len(duplicate_groups)} groups of duplicate files:")
            for file_hash, files in duplicate_groups.items():
                print(f"  Hash: {file_hash[:8]}...")
                for f in files:
                    print(f"    - {f['path']} ({f['size'] / 1024:.1f} KB)")
        else:
            print("\nNo duplicate files found.")

    if not (args.old_days or args.min_size_mb or args.find_duplicates):
        print("No criteria specified. Use --old-days, --min-size-mb, or --find-duplicates.")
    elif not old_files and not large_files and not duplicate_groups: # Check if all lists are empty
        print("\nAll clear! Your digital landscape is free of significant data dust.")

if __name__ == "__main__":
    main()
