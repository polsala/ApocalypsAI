import argparse
import os
import shutil
import fnmatch
from pathlib import Path
from typing import List, Set

DEFAULT_INCLUDE_PATTERNS = [
    "**/__pycache__",
    "**/.pytest_cache",
    "**/.mypy_cache",
    "**/.venv",
    "**/env",
    "**/node_modules",
    "**/target",  # Rust, Maven
    "**/build",   # C++, Java, Go
    "**/dist",    # Python, JS
    "**/out",
    "**/*.tmp",
]

DEFAULT_EXCLUDE_PATTERNS = [
    "**/.git/**",
    "**/.svn/**",
    "**/.hg/**",
    "**/.vscode/**",
    "**/.idea/**",
]

def get_size_of_path(path: Path) -> int:
    """Recursively get the size of a file or directory."""
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        total_size = 0
        for entry in path.rglob("*"):
            if entry.is_file():
                total_size += entry.stat().st_size
        return total_size
    return 0

def find_and_clean_caches(
    root_path: Path,
    include_patterns: List[str],
    exclude_patterns: List[str],
    dry_run: bool,
) -> int:
    """Finds cache directories and files based on patterns and optionally cleans them."""
    print(f"\n🌌 Initiating Cosmic Cache Scan in: {root_path}")
    print(f"✨ Including patterns: {include_patterns}")
    print(f"🚫 Excluding patterns: {exclude_patterns}")

    to_delete: Set[Path] = set()
    total_reclaimed_size = 0

    # First, find all potential candidates based on include patterns
    potential_candidates: Set[Path] = set()
    for pattern in include_patterns:
        for found_path in root_path.rglob(pattern):
            potential_candidates.add(found_path)

    # Filter out paths that match exclude patterns
    for candidate in potential_candidates:
        is_excluded = False
        # Check if the candidate itself or any of its parents match an exclude pattern
        for exclude_pattern in exclude_patterns:
            if fnmatch.fnmatch(str(candidate), exclude_pattern) or \
               any(fnmatch.fnmatch(str(p), exclude_pattern) for p in candidate.parents):
                is_excluded = True
                break
        if not is_excluded:
            to_delete.add(candidate)

    if not to_delete:
        print("🌠 No cosmic debris found to clean. Your system is pristine!")
        return 0

    print(f"\n🔭 Found {len(to_delete)} potential cosmic debris clusters:")
    for item_path in sorted(list(to_delete)):
        size = get_size_of_path(item_path)
        total_reclaimed_size += size
        size_mb = size / (1024 * 1024)
        action = "Would delete" if dry_run else "Deleting"
        print(f"  [{action}] {item_path} ({size_mb:.2f} MB)")

    if not dry_run:
        print("\n🚀 Initiating cosmic purge...")
        for item_path in sorted(list(to_delete)):
            try:
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                elif item_path.is_file():
                    os.remove(item_path)
                print(f"  ✅ Purged: {item_path}")
            except OSError as e:
                print(f"  ❌ Failed to purge {item_path}: {e}")
    else:
        print("\n✨ Dry run complete. No files were actually deleted.")

    total_reclaimed_mb = total_reclaimed_size / (1024 * 1024)
    print(f"\n✅ Cosmic Cache Cleaner finished. Reclaimed: {total_reclaimed_mb:.2f} MB")
    return total_reclaimed_size

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Cache Cleaner: Purge temporary files and cache directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Root path to start scanning from (default: current directory)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, listing files to be deleted without actually deleting them."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the deletion of identified files and directories."
    )
    parser.add_argument(
        "--include",
        nargs='*', # 0 or more arguments
        default=[],
        help="Glob patterns to include (e.g., '**/__pycache__'). Overrides defaults if provided."
    )
    parser.add_argument(
        "--exclude",
        nargs='*', # 0 or more arguments
        default=[],
        help="Glob patterns to exclude (e.g., '**/.git/**'). Overrides defaults if provided."
    )

    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("Error: Please specify either --dry-run or --execute.")
        parser.print_help()
        exit(1)

    if args.dry_run and args.execute:
        print("Error: Cannot specify both --dry-run and --execute.")
        parser.print_help()
        exit(1)

    root_path = Path(args.path).resolve()
    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist.")
        exit(1)

    include_patterns = args.include if args.include else DEFAULT_INCLUDE_PATTERNS
    exclude_patterns = args.exclude if args.exclude else DEFAULT_EXCLUDE_PATTERNS

    find_and_clean_caches(root_path, include_patterns, exclude_patterns, args.dry_run)

if __name__ == "__main__":
    main()
