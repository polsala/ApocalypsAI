import os
import argparse
import datetime

def get_file_info(filepath):
    """Returns a tuple of (modification_timestamp, size_in_bytes)."""
    try:
        stat = os.stat(filepath)
        return stat.st_mtime, stat.st_size
    except OSError:
        return None, None

def is_dust_bunny(filepath, current_time, age_days, min_size_bytes):
    """Determines if a file qualifies as a 'digital dust bunny'."""
    mod_time_stamp, size_bytes = get_file_info(filepath)

    if mod_time_stamp is None or size_bytes is None:
        return False # File not found or inaccessible

    # Check age
    mod_datetime = datetime.datetime.fromtimestamp(mod_time_stamp)
    age_delta = current_time - mod_datetime
    if age_delta.days < age_days:
        return False

    # Check size
    if size_bytes < min_size_bytes:
        return False

    return True

def generate_whimsical_suggestion(filepath, mod_datetime, size_bytes):
    """Generates a whimsical suggestion for a dust bunny file.
    The suggestion is deterministic based on the filepath for consistent testing.
    """
    suggestions = [
        f'"A relic from a forgotten era. Perhaps it\'s time for this digital fossil to return to the byte-dust it came from?"',
        f'"This digital tumbleweed has been rolling around for a while. Is it still serving a purpose, or just collecting virtual lint?"',
        f'"A spectral image from the past. Does it still spark joy, or just occupy space in your digital catacombs?"',
        f'"By the ancient digital scrolls, this file has seen many sunrises. Is its wisdom still relevant, or merely historical?"',
        f'"This file carries the scent of ages. Consider if its presence is a blessing or a burden to your digital ecosystem."'
    ]
    # Simple hash based on filepath to make suggestions deterministic for a given file
    suggestion_index = hash(filepath) % len(suggestions)
    return suggestions[suggestion_index]

def find_digital_dust_bunnies(target_path, age_days, min_size_kb):
    """Scans the target path for digital dust bunnies and returns their info."""
    dust_bunnies = []
    min_size_bytes = min_size_kb * 1024
    current_time = datetime.datetime.now()

    if not os.path.isdir(target_path):
        print(f"Error: Directory not found at '{target_path}'")
        return []

    print(f"Scanning {target_path} for digital dust bunnies...")

    for root, _, files in os.walk(target_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_dust_bunny(filepath, current_time, age_days, min_size_bytes):
                mod_time_stamp, size_bytes = get_file_info(filepath)
                mod_datetime = datetime.datetime.fromtimestamp(mod_time_stamp)
                dust_bunnies.append({
                    'filepath': filepath,
                    'mod_datetime': mod_datetime,
                    'size_bytes': size_bytes
                })
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify and suggest cleanup for old, large files (digital dust bunnies)."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The directory to scan for digital dust bunnies."
    )
    parser.add_argument(
        "--age", 
        type=int, 
        default=365, 
        help="Files older than this many days will be flagged (default: 365)."
    )
    parser.add_argument(
        "--min-size", 
        type=int, 
        default=1024, 
        help="Files smaller than this size (in KB) will be ignored (default: 1024)."
    )

    args = parser.parse_args()

    dust_bunnies = find_digital_dust_bunnies(
        args.path, args.age, args.min_size
    )

    if not dust_bunnies:
        print("\nNo digital dust bunnies found. Your digital realm is pristine! ✨")
        return

    print(f"\nFound {len(dust_bunnies)} potential digital dust bunnies:\n")
    for bunny in dust_bunnies:
        mod_date_str = bunny['mod_datetime'].strftime('%Y-%m-%d')
        size_mb = bunny['size_bytes'] / (1024 * 1024)
        suggestion = generate_whimsical_suggestion(bunny['filepath'], bunny['mod_datetime'], bunny['size_bytes'])
        print(f"*   [{mod_date_str}] {size_mb:.1f} MB - {bunny['filepath']}\n    -> {suggestion}")

    print(f"\nCleanup suggested for {len(dust_bunnies)} files. Proceed with caution, and may your storage be ever lean!")

if __name__ == "__main__":
    main()
