import os
import shutil
import argparse
from pathlib import Path
from typing import List

DEFAULT_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
    "*.log",
    "*.tmp",
    "node_modules",
    "target", # Common for Rust/Java builds
    "dist",
    "build",
    ".coverage",
    ".venv", # Use with caution!
]

def find_debris(root_path: Path, patterns: List[str]) -> List[Path]:
    """
    Finds files and directories matching the given patterns within the root_path.
    """
    debris_found = set() # Use a set to automatically handle duplicates
    for pattern in patterns:
        for item in root_path.rglob(pattern):
            # rglob finds both files and directories matching the pattern.
            # Add all matches to the set.
            debris_found.add(item)
    return sorted(list(debris_found)) # Convert to list and sort for consistent output

def sweep_debris(root_path: Path, patterns: List[str], dry_run: bool = False):
    """
    Sweeps (deletes) files and directories matching patterns.
    """
    print(f"🌌 Initiating Nightly Data Debris Sweep in: {root_path.resolve()}")
    print(f"🧹 Targeting patterns: {', '.join(patterns)}")
    print(f"{'[DRY RUN] ' if dry_run else ''}Scanning for debris...")

    debris_to_sweep = find_debris(root_path, patterns)

    if not debris_to_sweep:
        print("✨ No data debris found. Your repository is pristine!")
        return

    print(f"\n--- Debris identified ({len(debris_to_sweep)} items) ---")
    for item in debris_to_sweep:
        print(f"- {item.relative_to(root_path)} {'(DIR)' if item.is_dir() else '(FILE)'}")

    if dry_run:
        print("\n[DRY RUN] No files or directories were deleted. To perform actual deletion, remove --dry-run.")
    else:
        print("\n--- Sweeping debris... ---")
        deleted_count = 0
        for item in debris_to_sweep:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"🗑️ Swept directory: {item.relative_to(root_path)}")
                elif item.is_file():
                    os.remove(item)
                    print(f"🗑️ Swept file: {item.relative_to(root_path)}")
                deleted_count += 1
            except OSError as e:
                print(f"❌ Failed to sweep {item.relative_to(root_path)}: {e}")
        print(f"\n✅ Sweep complete! {deleted_count} items of debris purged.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Debris Sweeper: Cleans up temporary files and build artifacts."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="The root directory to start sweeping from. Defaults to current directory."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, the utility will only report what *would* be deleted without actually deleting anything."
    )
    parser.add_argument(
        "--patterns",
        nargs=",", # Changed from '+' to ',' to allow comma-separated patterns in a single string, or multiple --patterns arguments. No, '+' is correct for space-separated. Reverting.
        help="A space-separated list of glob patterns (e.g., '*.log', '__pycache__'). Overrides default patterns."
    )

    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    if not root_path.is_dir():
        print(f"Error: Path '{root_path}' is not a valid directory.")
        exit(1)

    patterns_to_use = args.patterns if args.patterns else DEFAULT_PATTERNS

    sweep_debris(root_path, patterns_to_use, args.dry_run)

if __name__ == "__main__":
    main()
