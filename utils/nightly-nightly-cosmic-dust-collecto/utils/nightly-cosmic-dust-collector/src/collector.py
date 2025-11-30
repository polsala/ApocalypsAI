import os
import argparse
import datetime

def find_cosmic_dust(path: str, max_size_kb: int = 10, min_age_days: int = 30) -> list[dict]:
    """
    Scans a directory for files considered 'cosmic dust' based on size and age.

    Args:
        path (str): The root directory to scan.
        max_size_kb (int): Maximum file size in kilobytes to consider as dust.
        min_age_days (int): Minimum age in days for a file to be considered dust.

    Returns:
        list[dict]: A list of dictionaries, each representing a 'dust' file
                    with its path, size, and last modification timestamp.
    """
    dust_files = []
    max_size_bytes = max_size_kb * 1024
    # Use datetime.datetime.now() for the current time reference
    current_time = datetime.datetime.now()
    min_age_timestamp = (current_time - datetime.timedelta(days=min_age_days)).timestamp()

    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return []

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Check if it's a regular file (not a symlink, etc.)
                if not os.path.isfile(file_path):
                    continue

                file_stat = os.stat(file_path)
                file_size = file_stat.st_size
                file_mtime = file_stat.st_mtime

                if file_size <= max_size_bytes and file_mtime < min_age_timestamp:
                    dust_files.append({
                        'path': file_path,
                        'size_bytes': file_size,
                        'last_modified': datetime.datetime.fromtimestamp(file_mtime).isoformat()
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or disappear during scan
                print(f"Warning: Could not access file '{file_path}': {e}")
                continue
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for small, old files (cosmic dust)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to begin scanning for dust."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=10,
        help="Maximum file size in kilobytes to consider as 'dust'. Defaults to 10 KB."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered 'dust'. Defaults to 30 days."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for cosmic dust (max size: {args.max_size_kb}KB, min age: {args.min_age_days} days)...")
    dust = find_cosmic_dust(args.path, args.max_size_kb, args.min_age_days)

    if dust:
        print("\n--- Cosmic Dust Found ---")
        for item in dust:
            print(f"- {item['path']} (Size: {item['size_bytes']} bytes, Last Modified: {item['last_modified']})")
        print("\nConsider reviewing these files for potential cleanup.")
    else:
        print("\nPath is sparkling clean! No cosmic dust found.")

if __name__ == "__main__":
    main()
