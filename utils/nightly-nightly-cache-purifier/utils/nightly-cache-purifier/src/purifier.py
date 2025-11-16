import os
import shutil
import platform
from datetime import datetime, timedelta
import argparse
from typing import List

def get_cache_dirs() -> List[str]:
    """Returns a list of common cache directories based on the OS."""
    dirs = []
    home = os.path.expanduser("~")

    if platform.system() == "Linux":
        dirs.append(os.path.join(home, ".cache"))
        dirs.append("/tmp")
    elif platform.system() == "Darwin":  # macOS
        dirs.append(os.path.join(home, "Library", "Caches"))
        dirs.append("/tmp")
    elif platform.system() == "Windows":
        temp_dir = os.environ.get("TEMP") or os.environ.get("TMP")
        if temp_dir:
            dirs.append(temp_dir)
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            dirs.append(os.path.join(local_app_data, "Temp"))
    
    # Filter out non-existent directories
    return [d for d in dirs if os.path.isdir(d)]

def clean_directory(directory: str, age_days: int, dry_run: bool, current_time: datetime) -> int:
    """
    Cleans files and empty directories in the given directory older than age_days.
    Returns the number of items (files/dirs) processed for deletion.
    """
    if not os.path.isdir(directory):
        print(f"Warning: Directory not found: {directory}")
        return 0

    print(f"Scanning: {directory}")
    deleted_count = 0
    cutoff_time = current_time - timedelta(days=age_days)

    for root, dirs, files in os.walk(directory, topdown=False): # topdown=False for deleting empty dirs
        # Process files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mod_time < cutoff_time:
                    if dry_run:
                        print(f"  [DRY RUN] Would delete file: {file_path} (modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
                    else:
                        os.remove(file_path)
                        print(f"  Deleted file: {file_path}")
                        deleted_count += 1
            except OSError as e:
                print(f"  Error processing file {file_path}: {e}")
        
        # Process empty directories (after files are potentially deleted)
        if not os.listdir(root): # Check if directory is empty
            if dry_run:
                print(f"  [DRY RUN] Would remove empty directory: {root}")
            else:
                try:
                    os.rmdir(root)
                    print(f"  Removed empty directory: {root}")
                    deleted_count += 1
                except OSError as e:
                    print(f"  Error removing directory {root}: {e}")

    return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Cache Purifier: Cleans old files from common cache directories."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=7,
        help="Delete files older than this many days. Default is 7 days."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deletion without actually removing files."
    )
    parser.add_argument(
        "--target-dir",
        type=str,
        help="Specify a custom directory to clean instead of default cache paths."
    )

    args = parser.parse_args()

    current_time = datetime.now()
    total_deleted = 0

    if args.target_dir:
        print(f"Cleaning specified directory: {args.target_dir}")
        total_deleted += clean_directory(args.target_dir, args.age_days, args.dry_run, current_time)
    else:
        cache_dirs = get_cache_dirs()
        if not cache_dirs:
            print("No common cache directories found for this OS.")
            return

        print(f"Cleaning common cache directories (files older than {args.age_days} days):")
        for cache_dir in cache_dirs:
            total_deleted += clean_directory(cache_dir, args.age_days, args.dry_run, current_time)

    mode = "[DRY RUN]" if args.dry_run else ""
    print(f"\n{mode} Purifier finished. Total items processed for deletion: {total_deleted}")

if __name__ == "__main__":
    main()
