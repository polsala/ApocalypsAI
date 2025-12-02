import os
import argparse
import datetime

def convert_bytes_to_mb(bytes_size):
    """Converts bytes to megabytes."""
    return bytes_size / (1024 * 1024)

def convert_mb_to_bytes(mb_size):
    """Converts megabytes to bytes."""
    return mb_size * (1024 * 1024)

def find_byte_blooms(root_dir, size_threshold_mb, age_threshold_days):
    """
    Scans a directory for files that are large and haven't been modified recently.

    Args:
        root_dir (str): The root directory to start scanning from.
        size_threshold_mb (int): Minimum file size in megabytes.
        age_threshold_days (int): Minimum age in days since last modification.

    Returns:
        list: A list of dictionaries, each representing a 'byte-bloom' file.
              Each dict contains 'path', 'size_mb', 'modified_date'.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found: {root_dir}")
        return []

    byte_blooms = []
    size_threshold_bytes = convert_mb_to_bytes(size_threshold_mb)
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=age_threshold_days)

    print(f"Scanning {root_dir} for byte-blooms (>= {size_threshold_mb} MB, >= {age_threshold_days} days old)...\n")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Get file stats
                stat = os.stat(file_path)
                file_size_bytes = stat.st_size
                file_mtime_timestamp = stat.st_mtime
                file_mtime_datetime = datetime.datetime.fromtimestamp(file_mtime_timestamp)

                # Check conditions
                if file_size_bytes >= size_threshold_bytes and file_mtime_datetime < cutoff_date:
                    byte_blooms.append({
                        'path': file_path,
                        'size_mb': round(convert_bytes_to_mb(file_size_bytes), 2),
                        'modified_date': file_mtime_datetime.strftime('%Y-%m-%d')
                    })
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.stat
                continue
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}")

    return byte_blooms

def main():
    parser = argparse.ArgumentParser(
        description="Identify large, infrequently modified files (byte-blooms) in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--size-mb",
        type=int,
        default=50,
        help="Minimum file size in megabytes to consider a 'byte-bloom'. (Default: 50 MB)"
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=60,
        help="Minimum age in days (since last modification) to consider a 'byte-bloom'. (Default: 60 days)"
    )

    args = parser.parse_args()

    blooms = find_byte_blooms(args.path, args.size_mb, args.age_days)

    if blooms:
        print(f"Found {len(blooms)} byte-blooms:\n")
        for bloom in blooms:
            print(f"- {bloom['path']} (Size: {bloom['size_mb']} MB, Modified: {bloom['modified_date']})")
        print("\nConsider pruning or replanting these forgotten byte-blooms to free up space!")
    else:
        print("No byte-blooms found matching the criteria. Your digital garden is pristine!")

if __name__ == "__main__":
    main()
