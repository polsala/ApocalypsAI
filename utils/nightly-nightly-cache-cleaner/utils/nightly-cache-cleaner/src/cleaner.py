import os
import shutil
import time
from datetime import datetime, timedelta

def find_stale_files(directory, age_days, size_mb):
    """
    Finds files in a directory that are older than age_days or larger than size_mb.
    """
    stale_files = []
    now = time.time()
    age_threshold_seconds = age_days * 24 * 60 * 60
    size_threshold_bytes = size_mb * 1024 * 1024

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_stat = os.stat(file_path)
                file_age_seconds = now - file_stat.st_mtime
                file_size_bytes = file_stat.st_size

                is_old = file_age_seconds > age_threshold_seconds
                is_large = file_size_bytes > size_threshold_bytes

                if is_old or is_large:
                    stale_files.append(file_path)
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.stat
                continue
            except Exception as e:
                print(f"Warning: Could not process '{file_path}': {e}")
    return stale_files

def archive_files(file_paths, archive_dir):
    """
    Moves a list of files to the specified archive directory.
    Creates the archive directory if it doesn't exist.
    """
    if not file_paths:
        print("No files to archive.")
        return []

    os.makedirs(archive_dir, exist_ok=True)
    archived_count = 0
    archived_files = []

    for file_path in file_paths:
        try:
            destination_path = os.path.join(archive_dir, os.path.basename(file_path))
            # Handle potential name collisions by appending a timestamp
            if os.path.exists(destination_path):
                name, ext = os.path.splitext(os.path.basename(file_path))
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                destination_path = os.path.join(archive_dir, f"{name}_{timestamp}{ext}")

            shutil.move(file_path, destination_path)
            archived_files.append(destination_path)
            archived_count += 1
            print(f"Archived: '{file_path}' -> '{destination_path}'")
        except Exception as e:
            print(f"Error archiving '{file_path}': {e}")
    print(f"Successfully archived {archived_count} out of {len(file_paths)} files.")
    return archived_files

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Nightly Cache Cleaner: Finds and archives stale or large files."
    )
    parser.add_argument(
        "directory",
        help="The root directory to scan for stale files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered stale (default: 30)."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=100,
        help="Files larger than this many MB will be considered stale (default: 100)."
    )
    parser.add_argument(
        "--archive-dir",
        help="Directory to move stale files to. If not specified, files are only listed.",
        default=None
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for files older than {args.age} days or larger than {args.size} MB...")
    stale_files = find_stale_files(args.directory, args.age, args.size)

    if stale_files:
        print("\n--- Found Stale Files ---")
        for f in stale_files:
            print(f)
        print(f"Total: {len(stale_files)} files.")

        if args.archive_dir:
            print(f"\n--- Archiving Files to '{args.archive_dir}' ---")
            archive_files(stale_files, args.archive_dir)
        else:
            print("\nTo archive these files, run again with --archive-dir <path>.")
    else:
        print("No stale files found matching the criteria.")

if __name__ == "__main__":
    main()
