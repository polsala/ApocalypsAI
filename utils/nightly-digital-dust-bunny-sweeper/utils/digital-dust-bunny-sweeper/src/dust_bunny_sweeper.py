import os
import argparse
import datetime

def get_file_info(filepath):
    """Returns (modification_timestamp, size_in_bytes) for a file."""
    try:
        stat = os.stat(filepath)
        return stat.st_mtime, stat.st_size
    except OSError:
        return None, None

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / (1024**2):.1f} MB"
    else:
        return f"{size_bytes / (1024**3):.1f} GB"

def find_dust_bunnies(root_path, age_threshold_days):
    """Scans the given path for files older than age_threshold_days and returns a list of them.
    Returns a list of tuples: (filepath, age_days, size_bytes).
    """
    dust_bunnies = []
    now = datetime.datetime.now()
    cutoff_date = now - datetime.timedelta(days=age_threshold_days)

    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            mtime_timestamp, size_bytes = get_file_info(filepath)

            if mtime_timestamp is None:
                continue # Skip files we can't stat

            mtime_dt = datetime.datetime.fromtimestamp(mtime_timestamp)
            if mtime_dt < cutoff_date:
                age_days = (now - mtime_dt).days
                dust_bunnies.append((filepath, age_days, size_bytes))
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify and suggest cleanup of old, unused files (digital dust bunnies)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for digital dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="The minimum age (in days) for a file to be considered a 'dust bunny'. (Default: 30)"
    )

    args = parser.parse_args()

    print(f"Scanning {args.path} for digital dust bunnies older than {args.age} days...\n")

    bunnies = find_dust_bunnies(args.path, args.age)

    if not bunnies:
        print("No digital dust bunnies found! Your repository is sparkling clean. ✨")
    else:
        print(f"Found {len(bunnies)} digital dust bunnies:\n")
        for filepath, age_days, size_bytes in bunnies:
            print(f"- 🗑️ {filepath} (Modified: {age_days} days ago, Size: {format_size(size_bytes)})")
        print("\nConsider these files for manual cleanup to maintain optimal repository hygiene!")

if __name__ == "__main__":
    main()
