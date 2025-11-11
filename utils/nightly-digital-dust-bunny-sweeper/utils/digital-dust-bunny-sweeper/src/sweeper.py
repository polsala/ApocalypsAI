import os
import time
import argparse

def convert_mb_to_bytes(mb):
    """Converts megabytes to bytes."""
    return mb * 1024 * 1024

def convert_days_to_seconds(days):
    """Converts days to seconds."""
    return days * 24 * 60 * 60

def find_dust_bunnies(path, age_days=30, min_size_mb=10):
    """ 
    Scans a directory for files older than age_days or larger than min_size_mb.

    Args:
        path (str): The root directory to scan.
        age_days (int): Files older than this many days will be flagged.
        min_size_mb (int): Files larger than this many megabytes will be flagged.

    Returns:
        list: A list of dictionaries, each representing a 'dust bunny' file.
              Each dict contains 'path', 'size_bytes', 'size_mb', 'age_days'.
    """
    dust_bunnies = []
    current_time = time.time()
    age_threshold_seconds = convert_days_to_seconds(age_days)
    size_threshold_bytes = convert_mb_to_bytes(min_size_mb)

    print(f"\nSweeping for digital dust bunnies in: '{path}'...")
    print(f"Looking for files older than {age_days} days OR larger than {min_size_mb} MB.\n")

    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist. No dust bunnies to sweep here!")
        return []
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a directory. Please provide a directory to sweep.")
        return []

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_stat = os.stat(file_path)
                file_size_bytes = file_stat.st_size
                file_mtime = file_stat.st_mtime

                is_old = (current_time - file_mtime) > age_threshold_seconds
                is_large = file_size_bytes > size_threshold_bytes

                if is_old or is_large:
                    age_in_days = round((current_time - file_mtime) / (24 * 60 * 60))
                    size_in_mb = round(file_size_bytes / (1024 * 1024), 2)
                    dust_bunnies.append({
                        'path': file_path,
                        'size_bytes': file_size_bytes,
                        'size_mb': size_in_mb,
                        'age_days': age_in_days
                    })
            except OSError as e:
                # Handle cases like permission denied or file disappeared during scan
                print(f"Warning: Could not access '{file_path}': {e}")
                continue
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Find old or large files."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age-days", 
        type=int, 
        default=30, 
        help="Files older than this many days will be flagged. Default: 30."
    )
    parser.add_argument(
        "--min-size-mb", 
        type=int, 
        default=10, 
        help="Files larger than this many megabytes will be flagged. Default: 10."
    )

    args = parser.parse_args()

    bunnies = find_dust_bunnies(args.path, args.age_days, args.min_size_mb)

    if bunnies:
        print("\n--- Digital Dust Bunny Report ---")
        for bunny in bunnies:
            print(f"  [!] Fluffy Dust Bunny Found: {bunny['path']}")
            print(f"      Size: {bunny['size_mb']} MB, Age: {bunny['age_days']} days")
        print(f"\nTotal digital dust bunnies swept: {len(bunnies)}")
        total_size_mb = sum(b['size_mb'] for b in bunnies)
        print(f"Estimated space reclaimable: {round(total_size_mb, 2)} MB")
        print("Consider giving these bunnies a new home (the recycle bin)!")
    else:
        print("\nNo digital dust bunnies found. Your digital space is sparkling clean!")

if __name__ == "__main__":
    main()
