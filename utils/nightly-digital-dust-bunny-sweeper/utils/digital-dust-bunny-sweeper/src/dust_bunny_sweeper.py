import os
import argparse
import datetime
import fnmatch
import sys

def get_current_time():
    """# Mock rationale: Allows deterministic testing of file age without relying on actual system time."""
    return datetime.datetime.now()

def find_dust_bunnies(
    root_path,
    age_days,
    patterns,
    dry_run,
    current_time_func=get_current_time
):
    """Scans the given path for empty directories and old files matching patterns.

    Args:
        root_path (str): The path to start scanning from.
        age_days (int): Files older than this many days will be flagged.
        patterns (list): List of glob patterns for files to flag (e.g., ['*.log', '*.tmp']).
        dry_run (bool): If True, only report, do not delete.
        current_time_func (callable): Function to get current time for mocking.

    Returns:
        tuple: (list of empty_dirs, list of old_files)
    """
    empty_dirs = []
    old_files = []
    now = current_time_func()
    cutoff_time = now - datetime.timedelta(days=age_days)

    print(f"\n🔍 Initiating 'Digital Dust Bunny' sweep in: {root_path}")
    print(f"⏳ Looking for files older than {age_days} days and empty directories.")
    if patterns:
        print(f"🎯 Targeting files matching patterns: {', '.join(patterns)}")
    if dry_run:
        print("👀 Dry run mode activated. No files will be harmed... yet.")
    else:
        print("💥 Deletion mode activated. Prepare for digital cleansing!")

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Check for empty directories
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)

        # Check for old files matching patterns
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # If patterns are specified, check if file matches any pattern
                if patterns and not any(fnmatch.fnmatch(filename, p) for p in patterns):
                    continue # Skip if patterns are specified and file doesn't match

                mod_timestamp = os.path.getmtime(file_path)
                mod_time = datetime.datetime.fromtimestamp(mod_timestamp)

                if mod_time < cutoff_time:
                    old_files.append(file_path)
            except OSError as e:
                print(f"⚠️  Warning: Could not access {file_path}: {e}", file=sys.stderr)

    return empty_dirs, old_files

def report_and_clean(
    empty_dirs,
    old_files,
    dry_run
):
    """Reports findings and optionally performs deletion.

    Args:
        empty_dirs (list): List of empty directory paths.
        old_files (list): List of old file paths.
        dry_run (bool): If True, only report, do not delete.
    """
    print("\n--- Digital Dust Bunny Report ---")

    if empty_dirs:
        print(f"\n👻 Found {len(empty_dirs)} spectral empty directories:")
        for d in empty_dirs:
            print(f"  - {d}")
        if not dry_run:
            print("\n🧹 Sweeping away empty directories...")
            for d in empty_dirs:
                try:
                    os.rmdir(d)
                    print(f"    ✅ Removed: {d}")
                except OSError as e:
                    print(f"    ❌ Failed to remove {d}: {e}", file=sys.stderr)
        else:
            print("\n(Dry run: Empty directories would be swept away.)")
    else:
        print("\n✨ No empty directories found. Your digital catacombs are pristine!")

    if old_files:
        print(f"\n🕰️ Found {len(old_files)} ancient data fragments:")
        for f in old_files:
            print(f"  - {f}")
        if not dry_run:
            print("\n🔥 Incinerating ancient data fragments...")
            for f in old_files:
                try:
                    os.remove(f)
                    print(f"    ✅ Incinerated: {f}")
                except OSError as e:
                    print(f"    ❌ Failed to incinerate {f}: {e}", file=sys.stderr)
        else:
            print("\n(Dry run: Ancient data fragments would be incinerated.)")
    else:
        print("\n🌟 No ancient data fragments found. Your archives are spick and span!")

    print("\n--- Sweep Complete ---")
    if not empty_dirs and not old_files:
        print("🎉 Your file system is remarkably clean. The apocalypse can wait!")
    elif dry_run:
        print("💡 Review the report above. Run again without --dry-run to perform actions.")
    else:
        print("✅ Digital dust bunnies vanquished! Your system is ready for anything.")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Clean up empty directories and old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root path to start scanning from. Defaults to current directory."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="Files older than this many days will be flagged for removal. Defaults to 30."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=[],
        help="Glob patterns for files to flag (e.g., '*.log', '*.tmp'). If empty, all old files are considered."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run: report what would be deleted without actually deleting anything."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified empty directories and old files. Use with caution!"
    )

    args = parser.parse_args()

    if args.delete and args.dry_run:
        print("Error: Cannot use --delete and --dry-run together. Choose one.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    empty_dirs, old_files = find_dust_bunnies(
        args.path,
        args.age_days,
        args.patterns,
        args.dry_run
    )

    # If --delete is not present, it's effectively a dry run for deletion actions
    report_and_clean(
        empty_dirs,
        old_files,
        args.dry_run or not args.delete
    )

if __name__ == "__main__":
    main()
