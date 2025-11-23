import os
import shutil
import argparse
from datetime import datetime, timedelta

def is_empty_file(filepath):
    """Checks if a file is empty."""
    return os.path.getsize(filepath) == 0

def is_small_file(filepath, max_size_bytes):
    """Checks if a file is smaller than a given size."""
    return os.path.getsize(filepath) < max_size_bytes

def is_old_temp_file(filepath, max_age_days, temp_patterns):
    """Checks if a file is an old temporary file based on patterns and age."""
    filename = os.path.basename(filepath).lower()
    is_temp = any(pattern in filename for pattern in temp_patterns)

    if not is_temp:
        return False

    try:
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        age = datetime.now() - mod_time
        return age > timedelta(days=max_age_days)
    except OSError:
        return False # File might have been deleted or inaccessible

def collect_dust(
    target_dir,
    dustbin_dir,
    dry_run=True,
    max_size_kb=1,
    max_age_days=30,
    temp_patterns=None
):
    """
    Scans target_dir for 'cosmic dust' files and optionally moves them to dustbin_dir.
    """
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return []

    if temp_patterns is None:
        temp_patterns = ['.tmp', '~', '#', '.bak', '.log']

    collected_files = []
    max_size_bytes = max_size_kb * 1024

    if not dry_run:
        os.makedirs(dustbin_dir, exist_ok=True)

    print(f"Scanning '{target_dir}' for cosmic dust...")
    print(f"  Max file size: {max_size_kb}KB")
    print(f"  Max temp file age: {max_age_days} days")
    print(f"  Temp file patterns: {', '.join(temp_patterns)}")
    print(f"  Mode: {'Dry Run' if dry_run else 'Move to ' + dustbin_dir}")

    for root, _, files in os.walk(target_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                if is_empty_file(filepath):
                    reason = "empty"
                elif is_small_file(filepath, max_size_bytes):
                    reason = f"small (<{max_size_kb}KB)"
                elif is_old_temp_file(filepath, max_age_days, temp_patterns):
                    reason = f"old temp (>{max_age_days} days)"
                else:
                    continue

                collected_files.append((filepath, reason))
                print(f"  [DUST] {filepath} ({reason})")

                if not dry_run:
                    relative_path = os.path.relpath(filepath, target_dir)
                    dest_path = os.path.join(dustbin_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(filepath, dest_path)
                    print(f"    Moved to: {dest_path}")

            except OSError as e:
                print(f"  Warning: Could not process '{filepath}': {e}")
            except Exception as e:
                print(f"  Unexpected error with '{filepath}': {e}")

    if not collected_files:
        print("No cosmic dust found. Your space is pristine!")
    else:
        print(f"\nCollected {len(collected_files)} pieces of cosmic dust.")
        if dry_run:
            print("Run with --move to actually move these files.")

    return collected_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans up small, forgotten, or old temporary files."
    )
    parser.add_argument(
        "--target-dir",
        required=True,
        help="The directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--dustbin-dir",
        required=True,
        help="The directory where collected dust will be moved."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=1,
        help="Maximum file size in kilobytes to consider as 'dust'. (Default: 1KB)"
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="Minimum age in days for temporary files to be considered 'dust'. (Default: 30 days)"
    )
    parser.add_argument(
        "--temp-patterns",
        type=lambda s: s.split(','),
        default='.tmp,~,#,.bak,.log',
        help="Comma-separated list of file extensions or patterns to identify temporary files. (Default: .tmp,~,#,.bak,.log)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Only list files that would be collected, without moving them. This is the default."
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Actually move the identified files to the dustbin directory. Overrides --dry-run."
    )

    args = parser.parse_args()

    dry_run = args.dry_run if not args.move else False

    collect_dust(
        target_dir=args.target_dir,
        dustbin_dir=args.dustbin_dir,
        dry_run=dry_run,
        max_size_kb=args.max_size_kb,
        max_age_days=args.max_age_days,
        temp_patterns=args.temp_patterns
    )

if __name__ == "__main__":
    main()
