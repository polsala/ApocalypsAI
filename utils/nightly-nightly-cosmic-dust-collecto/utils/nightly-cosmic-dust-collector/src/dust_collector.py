import os
import time
import datetime
import argparse
from typing import List, Dict, Any

def collect_dust(
    path: str,
    max_size_bytes: int = 1024 * 1024,  # 1MB
    min_age_days: int = 30,
    include_empty: bool = True,
    exclude_dirs: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Scans a directory for "cosmic dust" files based on size, age, and emptiness.

    Args:
        path (str): The root directory to scan.
        max_size_bytes (int): Maximum file size in bytes to consider as dust.
        min_age_days (int): Minimum age in days for a file to be considered dust.
        include_empty (bool): Whether to include empty files in the dust collection.
        exclude_dirs (List[str]): List of directory names to exclude from scanning.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a dust file.
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Path '{path}' does not exist or is not a directory.")

    dust_files = []
    current_time = time.time()
    min_mtime_timestamp = current_time - (min_age_days * 24 * 60 * 60)

    if exclude_dirs is None:
        exclude_dirs = []

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prune directories that are in the exclude_dirs list
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat = os.stat(file_path)
                file_size = stat.st_size
                file_mtime = stat.st_mtime

                is_dust = False
                # Check if file meets size and age criteria
                if file_size <= max_size_bytes and file_mtime < min_mtime_timestamp:
                    # If it's not empty, or if empty files are included, it's dust
                    if include_empty or file_size > 0:
                        is_dust = True
                # Special case: if it's an empty file and empty files are included, and it meets age criteria
                elif include_empty and file_size == 0 and file_mtime < min_mtime_timestamp:
                    is_dust = True

                if is_dust:
                    dust_files.append({
                        "path": file_path,
                        "size_bytes": file_size,
                        "last_modified": datetime.datetime.fromtimestamp(file_mtime).isoformat(),
                        "age_days": round((current_time - file_mtime) / (24 * 60 * 60), 2)
                    })
            except OSError:
                # File might have been deleted or become inaccessible between os.walk and os.stat
                continue
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans directories for small, old, or empty files."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024, # in KB
        help="Maximum file size in KB to consider as dust (default: 1024KB / 1MB)."
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=30, # in days
        help="Minimum age in days for a file to be considered dust (default: 30 days)."
    )
    parser.add_argument(
        "--no-empty",
        action="store_true",
        help="Do NOT include empty files in the dust collection."
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs='*',
        default=[],
        help="List of directory names to exclude from scanning (e.g., .git node_modules)."
    )

    args = parser.parse_args()

    try:
        dust = collect_dust(
            path=args.path,
            max_size_bytes=args.max_size * 1024, # Convert KB to bytes
            min_age_days=args.min_age,
            include_empty=not args.no_empty,
            exclude_dirs=args.exclude_dirs
        )

        if dust:
            print(f"🌌 Cosmic Dust Report for '{args.path}':")
            for item in dust:
                print(f"- Path: {item['path']}")
                print(f"  Size: {item['size_bytes']} bytes")
                print(f"  Last Modified: {item['last_modified']} ({item['age_days']} days old)")
                print("-" * 20)
            print(f"\nTotal {len(dust)} dust particles collected.")
        else:
            print(f"✨ No cosmic dust found in '{args.path}' matching criteria.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
