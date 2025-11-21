import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

def get_file_age_days(filepath: Path) -> float:
    """Calculates the age of a file in days."""
    # Mock rationale: In tests, this function will be mocked to return controlled ages
    # for simulated files, ensuring deterministic results without actual filesystem access.
    try:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        return (datetime.now() - mtime).days
    except FileNotFoundError:
        return -1 # Indicate file not found or inaccessible

def scan_directory(directory: Path, age_threshold_days: int) -> list[Path]:
    """
    Scans a directory for files older than the specified age threshold.
    Returns a list of paths to old files.
    """
    old_files = []
    if not directory.is_dir():
        print(f"🌌 Warning: Rift detected at '{directory}' - not a valid directory. Skipping.", file=sys.stderr)
        return old_files

    print(f"🔍 Scanning the temporal currents in '{directory}' for ancient data fragments...")
    for item in directory.iterdir():
        if item.is_file():
            age = get_file_age_days(item)
            if age >= age_threshold_days:
                old_files.append(item)
        elif item.is_dir():
            # Optionally, recurse into subdirectories. For simplicity, let's keep it flat for now.
            # If recursion is desired, add a --recursive flag and modify this.
            pass
    return old_files

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Tear Tidy-Upper: Mend the rifts in your filesystem by purging old files."
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        required=True,
        help="One or more directories to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be flagged. Default is 30 days."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the utility will only list files that *would* be deleted, without actually deleting them."
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="If present (and --dry-run` is absent), the utility will proceed with deletion without further prompt. Use with caution!"
    )

    args = parser.parse_args()

    target_directories = [Path(d).expanduser().resolve() for d in args.dirs]
    age_threshold = args.age
    dry_run = args.dry_run
    confirm_deletion = args.confirm

    all_old_files: list[Path] = []
    for directory in target_directories:
        all_old_files.extend(scan_directory(directory, age_threshold))

    if not all_old_files:
        print(f"\n✨ The temporal fabric is pristine! No tears older than {age_threshold} days found.")
        sys.exit(0)

    print(f"\n📜 Identified {len(all_old_files)} temporal tears (files older than {age_threshold} days):")
    for f in all_old_files:
        print(f"  - {f} (Age: {get_file_age_days(f)} days)")

    if dry_run:
        print("\n👁️ This was a dry run. No files were actually deleted. The tears persist for now.")
    else:
        if not confirm_deletion:
            response = input(f"\n⚠️ Proceed with mending {len(all_old_files)} temporal tears? (y/N): ").strip().lower()
            if response != 'y':
                print("🚫 Mending aborted. The tears remain.")
                sys.exit(2) # No-op exit code
        
        print("\n🩹 Mending temporal tears...")
        deleted_count = 0
        for f in all_old_files:
            try:
                # Mock rationale: In tests, Path.unlink() will be mocked to prevent actual file deletion,
                # ensuring tests are safe and deterministic.
                f.unlink()
                print(f"  ✅ Mended: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  ❌ Failed to mend {f}: {e}", file=sys.stderr)
        
        print(f"\n🎉 Successfully mended {deleted_count} temporal tears.")
        if deleted_count < len(all_old_files):
            print(f"⚠️ {len(all_old_files) - deleted_count} tears resisted mending.")
        sys.exit(0)

if __name__ == "__main__":
    main()
