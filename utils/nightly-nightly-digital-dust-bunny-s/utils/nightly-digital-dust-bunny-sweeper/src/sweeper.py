import os
import argparse
import sys

def clean_empty_dirs(root_dir: str, dry_run: bool = False) -> list[str]:
    """
    Recursively finds and removes empty directories within the given root_dir.

    Args:
        root_dir: The starting directory to scan.
        dry_run: If True, only report empty directories without deleting them.

    Returns:
        A list of paths to directories that were removed (or would be removed in dry-run).
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' does not exist or is not a directory.", file=sys.stderr)
        return []

    removed_dirs = []
    # Walk from the bottom up to ensure child empty directories are removed first.
    # This is crucial because if a parent directory becomes empty after its children
    # are removed, it can then be removed itself.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Check if the current directory is empty after its children have been processed.
        # os.listdir() is used here to get the *current* contents, not the snapshot from os.walk.
        # This is crucial because os.walk's dirnames/filenames are a snapshot at the start of the walk.
        # If a child directory was removed, it won't be in dirnames, but the parent might still be empty.
        try:
            current_contents = os.listdir(dirpath)
        except OSError as e:
            print(f"Warning: Could not list contents of '{dirpath}': {e}", file=sys.stderr)
            continue

        if not current_contents:
            if os.path.abspath(dirpath) == os.path.abspath(root_dir):
                # Don't remove the root directory itself, even if it becomes empty
                continue
            
            if dry_run:
                print(f"[DRY RUN] Would remove empty directory: {dirpath}")
            else:
                try:
                    os.rmdir(dirpath)
                    print(f"Removed empty directory: {dirpath}")
                except OSError as e:
                    print(f"Error removing directory '{dirpath}': {e}", file=sys.stderr)
                    continue
            removed_dirs.append(dirpath)
    
    return removed_dirs

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Recursively removes empty directories."
    )
    parser.add_argument(
        "root_dir",
        nargs="?", # Make it optional, default to current directory
        default=".",
        help="The root directory to start sweeping from. Defaults to current directory."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run: report empty directories without deleting them."
    )
    args = parser.parse_args()

    print(f"Starting Digital Dust Bunny Sweeper in '{os.path.abspath(args.root_dir)}'...")
    if args.dry_run:
        print("--- DRY RUN MODE ---")

    removed_count = len(clean_empty_dirs(args.root_dir, args.dry_run))

    if removed_count > 0:
        print(f"\nSweeper finished. {'Would have removed' if args.dry_run else 'Removed'} {removed_count} empty director{'y' if removed_count == 1 else 'ies'}.")
    else:
        print("\nSweeper finished. No empty directories found (or would be removed).")

if __name__ == "__main__":
    main()
