import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def get_file_age_days(filepath: Path) -> float:
    """Calculates the age of a file in days."""
    try:
        # On some systems, st_birthtime (creation time) might not be available.
        # st_mtime (modification time) is a more reliable fallback.
        # We prioritize creation time if available, otherwise modification time.
        # Mock rationale: os.stat is a system call. Mocking it allows controlling file metadata
        # like creation/modification times for deterministic testing without actual file system changes.
        stat_info = filepath.stat()
        if hasattr(stat_info, 'st_birthtime') and stat_info.st_birthtime is not None:
            file_timestamp = stat_info.st_birthtime
        else:
            file_timestamp = stat_info.st_mtime
        
        current_timestamp = time.time() # Mock rationale: time.time() is non-deterministic. Mocking it allows fixing the "current time" for tests.
        return (current_timestamp - file_timestamp) / (60 * 60 * 24)
    except FileNotFoundError:
        return -1 # File doesn't exist, effectively "not old enough" for deletion
    except OSError:
        # Handle other OS errors, e.g., permission denied
        return -1

def find_dust_bunnies(
    directory: Path,
    patterns: list[str],
    age_days: int
) -> list[Path]:
    """
    Finds files matching patterns and older than a specified age in days.
    """
    if not directory.is_dir():
        print(f"Error: Directory '{directory}' not found or is not a directory.", file=sys.stderr)
        return []

    dust_bunnies = []
    for pattern in patterns:
        # Mock rationale: Path.glob is a file system operation. Mocking it allows simulating
        # directory contents and file names for deterministic testing.
        for filepath in directory.glob(f"**/{pattern}"):
            if filepath.is_file():
                if get_file_age_days(filepath) >= age_days:
                    dust_bunnies.append(filepath)
    return dust_bunnies

def sweep_dust_bunnies(
    files_to_delete: list[Path],
    dry_run: bool,
    force: bool
) -> None:
    """
    Deletes the specified files, with dry-run and confirmation options.
    """
    if not files_to_delete:
        print("No digital dust bunnies found to sweep. Your system is sparkling clean!")
        return

    print(f"\nFound {len(files_to_delete)} digital dust bunnies:")
    for f in files_to_delete:
        print(f"  - {f} (Age: {get_file_age_days(f):.2f} days)")

    if dry_run:
        print("\nThis was a DRY RUN. No files were actually deleted.")
        return

    if not force:
        # Mock rationale: input() is interactive. Mocking it allows providing predefined
        # responses for deterministic testing without user intervention.
        confirmation = input("\nProceed with deletion? (y/N): ").strip().lower()
        if confirmation != 'y':
            print("Deletion cancelled.")
            return

    print("\nSweeping digital dust bunnies...")
    deleted_count = 0
    for f in files_to_delete:
        try:
            # Mock rationale: os.remove is a file system operation. Mocking it prevents
            # actual file deletion during tests and allows verifying calls.
            os.remove(f)
            print(f"  ✅ Deleted: {f}")
            deleted_count += 1
        except OSError as e:
            print(f"  ❌ Failed to delete {f}: {e}", file=sys.stderr)
    
    print(f"\nSweeping complete. {deleted_count} files deleted.")

def main():
    parser = argparse.ArgumentParser(
        description="Clean up old, unused, or temporary files."
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-p", "--pattern",
        action="append",
        default=[],
        help="File pattern to match (e.g., '*.tmp', 'backup_*', can be repeated)"
    )
    parser.add_argument(
        "-a", "--age-days",
        type=int,
        default=30,
        help="Delete files older than this many days (default: 30)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deletion without actually removing files."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip interactive confirmation for deletion."
    )

    args = parser.parse_args()

    if not args.pattern:
        print("Error: At least one --pattern must be specified.", file=sys.stderr)
        sys.exit(1)

    target_directory = Path(args.directory).resolve()

    files_to_delete = find_dust_bunnies(
        target_directory,
        args.pattern,
        args.age_days
    )

    sweep_dust_bunnies(files_to_delete, args.dry_run, args.force)

if __name__ == "__main__":
    main()
