import os
import time
import argparse
from datetime import datetime, timedelta
import fnmatch

def collect_dust(path: str, age_days: int = 30, patterns: list[str] = None, exclude_dirs: list[str] = None) -> list[dict]:
    """
    Scans a directory for files considered "cosmic dust" based on age and patterns.

    Args:
        path (str): The root directory to scan.
        age_days (int): Minimum age in days for a file to be considered dust.
        patterns (list[str], optional): List of glob patterns to match filenames.
                                        If None or empty, all files older than age_days are considered.
        exclude_dirs (list[str], optional): List of directory names to exclude from the scan.

    Returns:
        list[dict]: A list of dictionaries, each representing a "dust" file with its path, size, and mtime.
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return []

    dust_files = []
    current_time = time.time()
    age_threshold_timestamp = current_time - (age_days * 24 * 60 * 60)

    exclude_dirs = [d.lower() for d in exclude_dirs] if exclude_dirs else []

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prune directories from the walk
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat = os.stat(file_path)
                mtime = stat.st_mtime
                file_size = stat.st_size

                # Check age
                if mtime < age_threshold_timestamp:
                    # Check patterns if provided
                    if not patterns or any(fnmatch.fnmatch(file_name, p) for p in patterns):
                        dust_files.append({
                            'path': file_path,
                            'size': file_size,
                            'mtime': mtime
                        })
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.stat
                continue
            except OSError as e:
                print(f"Warning: Could not stat file '{file_path}': {e}")
                continue

    return dust_files

def format_size(size_bytes: int) -> str:
    """Formats file size into human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Finds old or temporary files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for dust."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="The minimum age in days for a file to be considered 'dust'. Defaults to 30."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=[],
        help="One or more glob patterns (e.g., '*.log', 'tmp_*') to match filenames. "
             "If no patterns are provided, all files older than the specified age will be considered."
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs='*',
        default=[],
        help="One or more directory names to exclude from the scan (e.g., '.git', 'node_modules')."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for cosmic dust (older than {args.age} days, patterns: {args.patterns if args.patterns else 'all files'})...")

    dust_files = collect_dust(args.path, args.age, args.patterns, args.exclude_dirs)

    if dust_files:
        print(f"\nCosmic Dust Report for {args.path}:")
        total_size = 0
        for file_info in sorted(dust_files, key=lambda x: x['path']):
            mtime_dt = datetime.fromtimestamp(file_info['mtime'])
            print(f"- {file_info['path']} ({format_size(file_info['size'])}, Last Modified: {mtime_dt.strftime('%Y-%m-%d')})")
            total_size += file_info['size']
        print(f"\nTotal dust found: {len(dust_files)} files, {format_size(total_size)}")
    else:
        print("\nNo cosmic dust found. Your repository is sparkling clean!")

if __name__ == "__main__":
    main()
