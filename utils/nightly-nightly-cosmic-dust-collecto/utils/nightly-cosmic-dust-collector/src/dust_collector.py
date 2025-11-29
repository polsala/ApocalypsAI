import os
import shutil
import time
import argparse
import fnmatch

def is_file_dust(file_path, min_age_days, max_size_kb, check_empty):
    """
    Determines if a file qualifies as 'dust' based on age, size, and emptiness.
    """
    try:
        stat = os.stat(file_path)
        file_size_bytes = stat.st_size
        file_mtime_seconds = stat.st_mtime

        is_dust = False

        # Check for emptiness
        if check_empty and file_size_bytes == 0:
            is_dust = True

        # Check for small size
        if max_size_kb is not None and file_size_bytes < max_size_kb * 1024:
            is_dust = True

        # Check for old age
        if min_age_days is not None:
            current_time = time.time()
            age_seconds = current_time - file_mtime_seconds
            age_days = age_seconds / (60 * 60 * 24)
            if age_days > min_age_days:
                is_dust = True

        return is_dust

    except OSError as e:
        print(f"Warning: Could not access file {file_path}: {e}")
        return False # Treat inaccessible files as not dust for safety

def scan_directory_for_dust(root_dir, min_age_days, max_size_kb, check_empty, ignore_patterns):
    """
    Scans a directory recursively for 'dust' files.
    Yields paths of identified dust files.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}")
        return

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out ignored directories first
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(os.path.join(dirpath, d), p) for p in ignore_patterns)]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Check if file path matches any ignore pattern
            if any(fnmatch.fnmatch(file_path, p) for p in ignore_patterns):
                continue

            if os.path.isfile(file_path) and is_file_dust(file_path, min_age_days, max_size_kb, check_empty):
                yield file_path

def quarantine_file(file_path, quarantine_dir):
    """
    Moves a file to the specified quarantine directory.
    """
    try:
        os.makedirs(quarantine_dir, exist_ok=True)
        destination_path = os.path.join(quarantine_dir, os.path.basename(file_path))
        # Handle potential name collisions by appending a timestamp/counter
        if os.path.exists(destination_path):
            base, ext = os.path.splitext(destination_path)
            destination_path = f"{base}_{int(time.time())}{ext}"

        shutil.move(file_path, destination_path)
        print(f"Quarantined: {file_path} -> {destination_path}")
        return True
    except Exception as e:
        print(f"Error quarantining {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Identify and quarantine old, small, or empty files."
    )
    parser.add_argument(
        "dirs",
        metavar="DIR",
        nargs="+",
        help="One or more directories to scan."
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=None,
        help="Minimum age in days for a file to be considered dust (e.g., 30 for 30 days old)."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="Maximum size in KB for a file to be considered dust (e.g., 1 for 1KB)."
    )
    parser.add_argument(
        "--empty",
        action="store_true",
        help="Consider empty files (0 bytes) as dust."
    )
    parser.add_argument(
        "--quarantine",
        metavar="QUARANTINE_DIR",
        help="Directory to move identified dust files to. If not specified, files are only listed."
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Glob patterns for files/directories to ignore (e.g., '.git/*' '*.log')."
    )

    args = parser.parse_args()

    if not any([args.min_age, args.max_size, args.empty]):
        parser.error("At least one of --min-age, --max-size, or --empty must be specified.")

    found_dust_count = 0
    for root_dir in args.dirs:
        print(f"Scanning '{root_dir}'...")
        for dust_file in scan_directory_for_dust(
            root_dir, args.min_age, args.max_size, args.empty, args.ignore
        ):
            found_dust_count += 1
            if args.quarantine:
                quarantine_file(dust_file, args.quarantine)
            else:
                print(f"Found dust: {dust_file}")

    if found_dust_count == 0:
        print("No cosmic dust found. Your digital space is pristine!")
    else:
        action = "quarantined" if args.quarantine else "identified"
        print(f"\nOperation complete. {found_dust_count} cosmic dust files {action}.")

if __name__ == "__main__":
    main()
