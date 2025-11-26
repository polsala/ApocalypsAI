import os
import shutil
import datetime
import argparse
import fnmatch
from typing import List, Optional

def is_file_old(filepath: str, age_threshold_days: int) -> bool:
    """Checks if a file is older than the specified threshold."""
    if not os.path.exists(filepath):
        return False
    
    try:
        mtime = os.path.getmtime(filepath)
        file_age_seconds = datetime.datetime.now().timestamp() - mtime
        file_age_days = file_age_seconds / (60 * 60 * 24)
        return file_age_days > age_threshold_days
    except OSError:
        # Handle cases where file might be inaccessible or metadata unreadable
        return False

def is_file_empty(filepath: str) -> bool:
    """Checks if a file is empty."""
    if not os.path.exists(filepath):
        return False
    
    try:
        return os.path.getsize(filepath) == 0
    except OSError:
        # Handle cases where file might be inaccessible
        return False

def matches_pattern(filename: str, patterns: Optional[List[str]]) -> bool:
    """Checks if a filename matches any of the given patterns."""
    if not patterns:
        return False
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False

def collect_cosmic_dust(
    root_dir: str,
    dustbin_dir: Optional[str] = None,
    dry_run: bool = True,
    age_threshold_days: int = 90,
    patterns: Optional[List[str]] = None
) -> List[str]:
    """
    Scans a directory for "cosmic dust" files (empty, old, or matching patterns).
    If not in dry_run mode, moves them to a specified dustbin directory.

    Args:
        root_dir: The directory to scan.
        dustbin_dir: The directory to move dust files to. Required if dry_run is False.
        dry_run: If True, only lists files; if False, moves them.
        age_threshold_days: Files older than this will be considered dust.
        patterns: List of fnmatch-style patterns (e.g., "*.tmp", "cache_*").

    Returns:
        A list of paths to the files identified as cosmic dust.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' does not exist or is not a directory.")
        return []

    if not dry_run and not dustbin_dir:
        print("Error: dustbin_dir must be specified when dry_run is False.")
        return []

    if dustbin_dir and not os.path.exists(dustbin_dir) and not dry_run:
        try:
            os.makedirs(dustbin_dir, exist_ok=True)
            print(f"Created dustbin directory: {dustbin_dir}")
        except OSError as e:
            print(f"Error creating dustbin directory '{dustbin_dir}': {e}")
            return []

    dust_files = []
    print(f"Scanning '{root_dir}' for cosmic dust (dry_run={dry_run})...")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            is_dust = False
            reasons = []

            if is_file_empty(filepath):
                is_dust = True
                reasons.append("empty")
            
            if age_threshold_days > 0 and is_file_old(filepath, age_threshold_days):
                is_dust = True
                reasons.append(f"older than {age_threshold_days} days")
            
            if patterns and matches_pattern(filename, patterns):
                is_dust = True
                reasons.append(f"matches pattern {filename}")

            if is_dust:
                dust_files.append(filepath)
                reason_str = ", ".join(reasons)
                if dry_run:
                    print(f"  [DRY RUN] Found dust: '{filepath}' ({reason_str})")
                else:
                    try:
                        dest_path = os.path.join(dustbin_dir, os.path.basename(filepath))
                        # Handle potential name collisions in dustbin
                        counter = 1
                        original_dest_path = dest_path
                        while os.path.exists(dest_path):
                            name, ext = os.path.splitext(original_dest_path)
                            dest_path = f"{name}_{counter}{ext}"
                            counter += 1

                        shutil.move(filepath, dest_path)
                        print(f"  Moved dust: '{filepath}' -> '{dest_path}' ({reason_str})")
                    except OSError as e:
                        print(f"  Error moving '{filepath}': {e}")
    
    print(f"Scan complete. Found {len(dust_files)} cosmic dust files.")
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans for and optionally moves old, empty, or patterned files."
    )
    parser.add_argument(
        "--root-dir",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--dustbin-dir",
        type=str,
        default=None,
        help="Optional: Directory to move identified dust files to. If not provided, files are only listed (dry run)."
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help="Perform actual file operations (move files) instead of just listing them."
    )
    parser.add_argument(
        "--age-threshold-days",
        type=int,
        default=90,
        help="Files older than this many days will be considered dust. Set to 0 to disable age check."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=[],
        help="List of fnmatch-style patterns (e.g., '*.tmp', 'cache_*') to identify dust files."
    )

    args = parser.parse_args()

    collect_cosmic_dust(
        root_dir=args.root_dir,
        dustbin_dir=args.dustbin_dir,
        dry_run=args.dry_run,
        age_threshold_days=args.age_threshold_days,
        patterns=args.patterns
    )

if __name__ == "__main__":
    main()
