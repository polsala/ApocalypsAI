import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import fnmatch

def is_older_than(path_stat, age_threshold_days):
    """Checks if a file/directory's modification time is older than the threshold."""
    if not path_stat:
        return False
    mod_timestamp = path_stat.st_mtime
    mod_datetime = datetime.fromtimestamp(mod_timestamp)
    return mod_datetime < (datetime.now() - timedelta(days=age_threshold_days))

def matches_patterns(path_name, include_patterns, exclude_patterns):
    """Checks if a path matches include/exclude patterns."""
    # If include patterns are specified, path must match at least one.
    if include_patterns:
        if not any(fnmatch.fnmatch(path_name, p) for p in include_patterns):
            return False
    # If exclude patterns are specified, path must not match any.
    if exclude_patterns:
        if any(fnmatch.fnmatch(path_name, p) for p in exclude_patterns):
            return False
    return True

def scan_directory(
    root_path: Path,
    age_threshold_days: int,
    include_patterns: list[str],
    exclude_patterns: list[str]
) -> list[tuple[Path, str]]:
    """Scans a directory for 'digital dust bunnies'."""
    dust_bunnies = []
    current_time = datetime.now()

    for item in root_path.rglob('*'): # rglob for recursive globbing
        try:
            item_stat = item.stat()
            is_file = item.is_file()
            is_dir = item.is_dir()

            # Check if it's an empty directory
            if is_dir and not any(item.iterdir()):
                dust_bunnies.append((item, "Empty Directory"))
                continue # An empty directory is a dust bunny regardless of age/patterns

            # For files and non-empty directories, check age and patterns
            # Only check non-empty dirs for age, as empty ones are handled above
            if is_file or (is_dir and any(item.iterdir())):
                if is_older_than(item_stat, age_threshold_days) and \
                   matches_patterns(item.name, include_patterns, exclude_patterns):
                    age_in_days = (current_time - datetime.fromtimestamp(item_stat.st_mtime)).days
                    dust_bunnies.append((item, f"{'File' if is_file else 'Directory'}, {age_in_days} days old"))

        except (OSError, PermissionError) as e:
            print(f"Warning: Could not access {item}: {e}", file=sys.stderr)
            continue

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify 'digital dust bunnies' (old/empty files and directories)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=365,
        help="Files/directories older than this many days will be flagged (default: 365)."
    )
    parser.add_argument(
        "--include",
        nargs='*',
        default=[],
        help="Glob patterns for files/directories to INCLUDE in the scan (e.g., '*.log', 'temp_*')."
    )
    parser.add_argument(
        "--exclude",
        nargs='*',
        default=[],
        help="Glob patterns for files/directories to EXCLUDE from the scan (e.g., '*.bak', 'node_modules')."
    )
    # dry-run is implicit as the utility only reports
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="(Implicit) This utility only reports findings and does not delete anything."
    )

    args = parser.parse_args()

    root_path = Path(args.path)
    if not root_path.is_dir():
        print(f"Error: Path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {root_path} for digital dust bunnies...")

    dust_bunnies = scan_directory(
        root_path,
        args.age,
        args.include,
        args.exclude
    )

    if dust_bunnies:
        print(f"\nFound {len(dust_bunnies)} digital dust bunnies:")
        for item_path, reason in dust_bunnies:
            print(f"- {item_path} ({reason})")
    else:
        print("\nNo digital dust bunnies found. Your filesystem is sparkling clean!")

    print("\nScan complete. No actual deletion performed (dry-run mode).")


if __name__ == "__main__":
    main()
