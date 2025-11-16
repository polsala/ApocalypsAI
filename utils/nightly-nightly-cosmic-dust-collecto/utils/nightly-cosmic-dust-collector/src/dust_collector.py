import os
import shutil
import argparse
import datetime
import sys

DEFAULT_MAX_SIZE_KB = 1  # 1 KB
DEFAULT_MIN_AGE_DAYS = 30 # 30 days

def is_dust_file(filepath, max_size_bytes, min_age_seconds, current_time):
    """Checks if a file qualifies as 'cosmic dust'."""
    try:
        stat_info = os.stat(filepath)
        file_size = stat_info.st_size
        file_mtime = stat_info.st_mtime

        is_empty = file_size == 0
        is_small = file_size <= max_size_bytes
        is_old = (current_time - file_mtime) > min_age_seconds

        # A file is dust if it's empty OR (small AND old)
        return is_empty or (is_small and is_old)
    except FileNotFoundError:
        return False # File might have been deleted between walk and stat
    except Exception as e:
        print(f"Error checking file {filepath}: {e}", file=sys.stderr)
        return False

def collect_dust(scan_path, quarantine_dir=None, max_size_kb=DEFAULT_MAX_SIZE_KB, min_age_days=DEFAULT_MIN_AGE_DAYS, report_only=False):
    """Scans for and optionally quarantines 'cosmic dust' files."""
    if not os.path.isdir(scan_path):
        print(f"Error: Scan path '{scan_path}' is not a valid directory.", file=sys.stderr)
        return None

    dust_files = []
    max_size_bytes = max_size_kb * 1024
    min_age_seconds = min_age_days * 24 * 60 * 60
    current_time = datetime.datetime.now().timestamp()

    if quarantine_dir and not report_only:
        os.makedirs(quarantine_dir, exist_ok=True)
        print(f"Quarantine directory: {quarantine_dir}")

    print(f"Scanning '{scan_path}' for cosmic dust (max size: {max_size_kb}KB, min age: {min_age_days} days)...")

    for root, _, files in os.walk(scan_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_dust_file(filepath, max_size_bytes, min_age_seconds, current_time):
                dust_files.append(filepath)
                if quarantine_dir and not report_only:
                    try:
                        dest_path = os.path.join(quarantine_dir, os.path.basename(filepath))
                        # Handle potential name collisions in quarantine
                        counter = 1
                        original_dest_path = dest_path
                        while os.path.exists(dest_path):
                            name, ext = os.path.splitext(os.path.basename(original_dest_path))
                            dest_path = os.path.join(quarantine_dir, f"{name}_{counter}{ext}")
                            counter += 1

                        shutil.move(filepath, dest_path)
                        print(f"  Moved: '{filepath}' -> '{dest_path}'")
                    except Exception as e:
                        print(f"  Error moving '{filepath}': {e}", file=sys.stderr)
                else:
                    print(f"  Found: '{filepath}'")

    if not dust_files:
        print("No cosmic dust found. Your repository is sparkling clean!")
    elif report_only:
        print(f"\n--- Cosmic Dust Report ({len(dust_files)} files) ---")
        for f in dust_files:
            print(f"- {f}")
        print("---------------------------------------")
    else:
        print(f"\nSuccessfully processed {len(dust_files)} cosmic dust files.")

    return dust_files

def main():
    parser = argparse.ArgumentParser(description="Nightly Cosmic Dust Collector: Scans for and optionally quarantines small, old, or empty files.")
    parser.add_argument('--path', type=str, required=True, help='The root directory to start scanning for dust.')
    parser.add_argument('--quarantine-dir', type=str, help='If provided, identified dust files will be moved here. If not provided, files will only be reported.')
    parser.add_argument('--max-size-kb', type=float, default=DEFAULT_MAX_SIZE_KB, help=f'Maximum file size in kilobytes to consider as dust. Defaults to {DEFAULT_MAX_SIZE_KB} KB.')
    parser.add_argument('--min-age-days', type=int, default=DEFAULT_MIN_AGE_DAYS, help=f'Minimum age in days for a file to be considered dust. Defaults to {DEFAULT_MIN_AGE_DAYS} days.')
    parser.add_argument('--report-only', action='store_true', help='If set, files will only be reported, even if --quarantine-dir is specified. This overrides the move action.')

    args = parser.parse_args()

    collected = collect_dust(
        scan_path=args.path,
        quarantine_dir=args.quarantine_dir,
        max_size_kb=args.max_size_kb,
        min_age_days=args.min_age_days,
        report_only=args.report_only
    )
    sys.exit(0 if collected is not None else 1) # Exit 0 for success (even if no dust), 1 for error

if __name__ == '__main__':
    main()
