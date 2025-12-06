import argparse
import os
import subprocess
import time
from datetime import datetime, timedelta

def parse_size(size_str):
    """Parses a human-readable size string (e.g., '100K', '5M', '1G') into bytes."""
    if not size_str:
        return 0
    size_str = size_str.upper()
    if size_str.endswith('K'):
        return int(size_str[:-1]) * 1024
    elif size_str.endswith('M'):
        return int(size_str[:-1]) * 1024 * 1024
    elif size_str.endswith('G'):
        return int(size_str[:-1]) * 1024 * 1024 * 1024
    return int(size_str)

def parse_duration(duration_str):
    """Parses a human-readable duration string (e.g., '7d', '30d', '1y') into a timedelta object."""
    if not duration_str:
        return timedelta(seconds=0) # No age limit
    duration_str = duration_str.lower()
    if duration_str.endswith('d'):
        return timedelta(days=int(duration_str[:-1]))
    elif duration_str.endswith('w'):
        return timedelta(weeks=int(duration_str[:-1]))
    elif duration_str.endswith('y'):
        return timedelta(days=int(duration_str[:-1]) * 365) # Approximate year
    return timedelta(seconds=0) # Default to no limit if invalid

def get_untracked_files(path):
    """Uses git to get a list of untracked files, excluding those ignored by .gitignore."""
    try:
        # --others: show untracked files
        # --exclude-standard: use .gitignore and other standard exclusions
        # -z: NUL-terminated output for safe parsing of filenames with spaces/newlines
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        # Split by NUL character and filter out empty strings
        return [f for f in result.stdout.split('\0') if f]
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"Stderr: {e.stderr}")
        return []
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return []

def find_dust(root_path, min_size_bytes, older_than_duration):
    """Finds 'cosmic dust' (untracked files) based on size and age criteria."""
    dust_files = []
    now = datetime.now()

    untracked_files = get_untracked_files(root_path)

    for rel_file_path in untracked_files:
        full_file_path = os.path.join(root_path, rel_file_path)
        if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
            continue # Skip if file doesn't exist or is not a regular file

        try:
            file_size = os.path.getsize(full_file_path)
            file_mtime_timestamp = os.path.getmtime(full_file_path)
            file_mtime = datetime.fromtimestamp(file_mtime_timestamp)

            # Check size criteria
            if file_size < min_size_bytes:
                continue

            # Check age criteria
            if older_than_duration.total_seconds() > 0 and (now - file_mtime) < older_than_duration:
                continue

            dust_files.append((full_file_path, file_size, file_mtime))
        except OSError as e:
            print(f"Warning: Could not access file {full_file_path}: {e}")
            continue

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Identify and clean up untracked, old, or large files."
    )
    parser.add_argument(
        '--path', type=str, default='.',
        help='The root directory to start scanning from. Defaults to current working directory.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Perform a dry run. Files will be identified and reported, but not deleted.'
    )
    parser.add_argument(
        '--min-size', type=str, default='0',
        help='Only consider files larger than this size (e.g., 100K, 5M, 1G). Default: 0.'
    )
    parser.add_argument(
        '--older-than', type=str, default='0d',
        help='Only consider files older than this duration (e.g., 7d, 30d, 1y). Default: 0d.'
    )
    parser.add_argument(
        '--delete', action='store_true',
        help='WARNING: Actually delete the identified files. Use with extreme caution and always after a --dry-run.'
    )

    args = parser.parse_args()

    min_size_bytes = parse_size(args.min_size)
    older_than_duration = parse_duration(args.older_than)

    print(f"\n--- Cosmic Dust Collector Report ---")
    print(f"Scanning path: {os.path.abspath(args.path)}")
    print(f"Minimum size: {args.min_size} ({min_size_bytes} bytes)")
    print(f"Older than: {args.older_than} ({older_than_duration})")
    print(f"Mode: {'Dry Run' if args.dry_run or not args.delete else 'DELETION'}\n")

    dust_files = find_dust(args.path, min_size_bytes, older_than_duration)

    if not dust_files:
        print("No cosmic dust found matching your criteria. Your repository is pristine!")
        return

    print(f"Found {len(dust_files)} potential 'cosmic dust' files:")
    total_size_freed = 0
    for file_path, file_size, file_mtime in dust_files:
        print(f"  - {file_path} ({(file_size / (1024*1024)):.2f} MB, Modified: {file_mtime.strftime('%Y-%m-%d')})")
        total_size_freed += file_size

    print(f"\nTotal size of cosmic dust: {(total_size_freed / (1024*1024)):.2f} MB")

    if args.delete and not args.dry_run:
        print("\n--- Deleting Cosmic Dust ---")
        for file_path, _, _ in dust_files:
            try:
                os.remove(file_path)
                print(f"  Deleted: {file_path}")
            except OSError as e:
                print(f"  Error deleting {file_path}: {e}")
        print("Cosmic dust successfully swept away!")
    else:
        print("\nThis was a dry run. No files were deleted. Use --delete to remove them.")

if __name__ == '__main__':
    main()
