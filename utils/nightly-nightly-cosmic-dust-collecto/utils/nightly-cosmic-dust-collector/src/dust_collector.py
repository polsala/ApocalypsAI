import os
import datetime
import shutil
import fnmatch
import argparse

def collect_dust(
    target_dir: str,
    age_days: int = 30,
    patterns: list[str] = None,
    archive_mode: bool = False,
    verbose: bool = True
) -> list[str]:
    """
    Identifies and optionally archives 'dust' files in a target directory.

    Args:
        target_dir: The root directory to scan.
        age_days: Files older than this many days will be considered dust.
        patterns: List of glob patterns to match filenames (e.g., '*.log', 'temp_*').
                  If None, all files are considered.
        archive_mode: If True, identified files are moved to an 'archive' subdirectory.
                      Otherwise, it's a dry run.
        verbose: If True, print detailed output.

    Returns:
        A list of paths to the files that were identified as dust.
    """
    if not os.path.isdir(target_dir):
        if verbose:
            print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return []

    cutoff_time = datetime.datetime.now() - datetime.timedelta(days=age_days)
    identified_dust_files = []

    archive_dir = os.path.join(target_dir, 'archive')
    if archive_mode and not os.path.exists(archive_dir):
        os.makedirs(archive_dir, exist_ok=True)
        if verbose:
            print(f"Created archive directory: {archive_dir}")

    if verbose:
        print(f"Scanning '{target_dir}' for files older than {age_days} days...")
        if patterns:
            print(f"Matching patterns: {', '.join(patterns)}")
        print(f"Mode: {'Archive' if archive_mode else 'Dry Run'}")

    for root, _, files in os.walk(target_dir):
        # Skip the archive directory itself to prevent infinite loops or archiving archives
        if root == archive_dir or root.startswith(archive_dir + os.sep):
            continue

        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if it's a file (and not a broken symlink, etc.)
            if not os.path.isfile(file_path):
                continue

            # Check age
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            except OSError:
                if verbose:
                    print(f"Warning: Could not get modification time for {file_path}. Skipping.")
                continue

            is_old = mtime < cutoff_time

            # Check pattern
            is_pattern_match = True
            if patterns:
                is_pattern_match = any(fnmatch.fnmatch(filename, p) for p in patterns)

            if is_old and is_pattern_match:
                identified_dust_files.append(file_path)
                if verbose:
                    print(f"  [DUST] {file_path} (Modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")

                if archive_mode:
                    try:
                        shutil.move(file_path, archive_dir)
                        if verbose:
                            print(f"    -> Archived to {os.path.join(archive_dir, filename)}")
                    except Exception as e:
                        if verbose:
                            print(f"    -> Error archiving {file_path}: {e}")

    if not identified_dust_files:
        if verbose:
            print("No cosmic dust found. Your directory is sparkling clean! ✨")
    elif not archive_mode and verbose:
        print("\nThis was a dry run. To archive these files, run with the --archive flag.")

    return identified_dust_files


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Identifies and archives old or specified files."
    )
    parser.add_argument(
        '--target-dir', 
        type=str, 
        required=True, 
        help='The root directory to scan for cosmic dust.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        default=30, 
        help='Files older than this many days will be considered dust. (Default: 30)'
    )
    parser.add_argument(
        '--patterns', 
        nargs='*', 
        default=None, 
        help='One or more glob patterns to match filenames (e.g., "*.log", "temp_*").'
             ' If not provided, all files are considered.'
    )
    parser.add_argument(
        '--archive', 
        action='store_true', 
        help='If set, identified files will be moved to an "archive" subdirectory within the target-dir. '
             'Otherwise, it\'s a dry run.'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        default=True, 
        help='Print detailed output (default: True).'
    )
    parser.add_argument(
        '--quiet', 
        action='store_false', 
        dest='verbose', 
        help='Suppress detailed output.'
    )

    args = parser.parse_args()

    collect_dust(
        target_dir=args.target_dir,
        age_days=args.age,
        patterns=args.patterns,
        archive_mode=args.archive,
        verbose=args.verbose
    )


if __name__ == '__main__':
    main()
