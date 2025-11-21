import os
import shutil
import argparse
from pathlib import Path
from typing import List, Set

DEFAULT_PATTERNS: List[str] = [
    "__pycache__",  # Python cache directories
    "*.pyc",        # Compiled Python files
    "*.pyo",        # Optimized Python files
    ".DS_Store",    # macOS specific metadata files
    "node_modules", # Node.js dependency directories
    "dist",         # Common build output directories
    "build",        # Common build output directories
    "target",       # Java/Rust build output directories
    ".vscode",      # VS Code configuration directories
    ".idea",        # IntelliJ IDEA configuration directories
    "*.log",        # Log files
    "*.tmp",        # Temporary files
    "*.bak",        # Backup files
]

def sweep_directory(
    root_path: Path,
    patterns: List[str],
    dry_run: bool = False
) -> List[Path]:
    """
    Sweeps a directory for files and directories matching specified patterns
    and removes them.

    Args:
        root_path: The root directory to start sweeping from.
        patterns: A list of glob-style patterns to match.
        dry_run: If True, only print what would be deleted, don't delete.

    Returns:
        A list of paths that were (or would be) deleted.
    """
    if not root_path.is_dir():
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    print(f"Sweeping '{root_path}' for digital dust bunnies...")
    print(f"Patterns to match: {patterns}")
    if dry_run:
        print("--- DRY RUN MODE --- No files will be deleted.")

    deleted_items: List[Path] = []
    all_patterns: Set[str] = set(patterns)

    for item_path in root_path.rglob("*"):
        # Check if the item itself matches any pattern
        # For directories, we check the directory name
        # For files, we check the file name
        match_found = False
        for pattern in all_patterns:
            if item_path.name == pattern: # Exact match for dir/file name
                match_found = True
                break
            if item_path.match(pattern): # Glob match for file name
                match_found = True
                break
        
        if match_found:
            if item_path.is_dir():
                print(f"  [DIR] {'Would delete' if dry_run else 'Deleting'}: {item_path}")
                if not dry_run:
                    try:
                        shutil.rmtree(item_path)
                        deleted_items.append(item_path)
                    except OSError as e:
                        print(f"    Error deleting directory {item_path}: {e}")
            elif item_path.is_file():
                print(f"  [FILE] {'Would delete' if dry_run else 'Deleting'}: {item_path}")
                if not dry_run:
                    try:
                        os.remove(item_path)
                        deleted_items.append(item_path)
                    except OSError as e:
                        print(f"    Error deleting file {item_path}: {e}")

    if not deleted_items:
        print("No digital dust bunnies found. Your repository is sparkling clean!")
    elif dry_run:
        print(f"Dry run complete. {len(deleted_items)} items would have been deleted.")
    else:
        print(f"Sweeping complete. {len(deleted_items)} items deleted.")

    return deleted_items

def main():
    parser = argparse.ArgumentParser(
        description="Sweeps a directory for common temporary files and build artifacts."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start sweeping from."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only print what would be deleted, without performing any actual deletions."
    )
    parser.add_argument(
        "--patterns",
        nargs="*",
        default=[],
        help="A space-separated list of additional patterns to include. These will be added to the default list."
    )

    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    all_patterns = list(set(DEFAULT_PATTERNS + args.patterns)) # Combine and deduplicate

    sweep_directory(root_path, all_patterns, args.dry_run)

if __name__ == "__main__":
    main()
