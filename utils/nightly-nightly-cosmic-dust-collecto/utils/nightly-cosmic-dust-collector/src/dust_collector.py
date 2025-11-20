import os
import time
import argparse
from datetime import datetime, timedelta

def collect_dust(
    target_dir: str,
    min_age_days: int = 30,
    max_size_kb: int = 10,
    include_extensions: list[str] = None,
    exclude_extensions: list[str] = None
) -> list[dict]:
    """
    Scans a directory for files considered "cosmic dust" based on age, size, and extensions.

    Args:
        target_dir: The root directory to scan.
        min_age_days: Files older than this many days are considered dust.
        max_size_kb: Files smaller than this many KB are considered dust.
        include_extensions: List of extensions to specifically include (e.g., ['.log', '.tmp']).
                            If None or empty, all extensions are considered.
        exclude_extensions: List of extensions to specifically exclude (e.g., ['.py', '.md']).

    Returns:
        A list of dictionaries, each representing a piece of "dust" found.
    """
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return []

    dust_files = []
    now = datetime.now()
    age_threshold_timestamp = (now - timedelta(days=min_age_days)).timestamp()
    max_size_bytes = max_size_kb * 1024

    if include_extensions:
        include_extensions = [ext.lower() for ext in include_extensions]
    if exclude_extensions:
        exclude_extensions = [ext.lower() for ext in exclude_extensions]

    print(f"Scanning '{target_dir}' for cosmic dust...")
    print(f"  - Older than: {min_age_days} days")
    print(f"  - Smaller than: {max_size_kb} KB")
    if include_extensions:
        print(f"  - Including extensions: {', '.join(include_extensions)}")
    if exclude_extensions:
        print(f"  - Excluding extensions: {', '.join(exclude_extensions)}")
    print("-" * 40)

    for root, _, files in os.walk(target_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat = os.stat(file_path)
                file_size = stat.st_size
                file_mtime = stat.st_mtime
                file_extension = os.path.splitext(file_name)[1].lower()

                # Check extension filters
                if include_extensions and file_extension not in include_extensions:
                    continue
                if exclude_extensions and file_extension in exclude_extensions:
                    continue

                # Check age and size
                is_old = file_mtime < age_threshold_timestamp
                is_small = file_size < max_size_bytes

                if is_old and is_small:
                    dust_files.append({
                        "path": file_path,
                        "size_bytes": file_size,
                        "last_modified": datetime.fromtimestamp(file_mtime).isoformat()
                    })
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.stat
                continue
            except Exception as e:
                print(f"Warning: Could not process '{file_path}': {e}")
                continue
    
    if not dust_files:
        print("No cosmic dust found. Your repository is sparkling clean!")
    else:
        print(f"\nFound {len(dust_files)} pieces of cosmic dust:")
        for dust in dust_files:
            print(f"  - Path: {dust['path']}")
            print(f"    Size: {dust['size_bytes']} bytes")
            print(f"    Last Modified: {dust['last_modified']}")
        print("\nConsider reviewing these files for potential cleanup.")

    return dust_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans directories for small, old, or empty files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=30,
        help="Files older than this many days will be considered 'dust'. Default: 30."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=10,
        help="Files smaller than this many kilobytes (KB) will be considered 'dust'. Default: 10."
    )
    parser.add_argument(
        "--include-ext",
        type=str,
        default="",
        help="Comma-separated list of file extensions to *include* in the scan (e.g., .log,.tmp). If empty, all extensions are considered."
    )
    parser.add_argument(
        "--exclude-ext",
        type=str,
        default="",
        help="Comma-separated list of file extensions to *exclude* from the scan (e.g., .py,.md)."
    )

    args = parser.parse_args()

    include_ext_list = [ext.strip() for ext in args.include_ext.split(',') if ext.strip()] if args.include_ext else None
    exclude_ext_list = [ext.strip() for ext in args.exclude_ext.split(',') if ext.strip()] if args.exclude_ext else None

    collect_dust(
        target_dir=args.path,
        min_age_days=args.min_age_days,
        max_size_kb=args.max_size_kb,
        include_extensions=include_ext_list,
        exclude_extensions=exclude_ext_list
    )
