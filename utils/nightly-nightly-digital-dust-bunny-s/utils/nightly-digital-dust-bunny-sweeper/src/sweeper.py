import os
import argparse
import sys

def clean_empty_dirs(root_dir: str, dry_run: bool = False) -> int:
    """
    Recursively cleans empty directories starting from root_dir.

    Args:
        root_dir: The path to the directory to start cleaning from.
        dry_run: If True, only report what would be done, don't actually delete.

    Returns:
        The number of directories deleted (or would be deleted in dry-run).
    """
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.", file=sys.stderr)
        return 0

    deleted_count = 0
    # Walk directories from bottom up to ensure child empty dirs are deleted first
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Check if the directory itself is empty (no files and no subdirectories left)
        # after potential deletions of subdirectories by earlier iterations of os.walk
        try:
            if not os.listdir(dirpath):
                action = "Would delete" if dry_run else "Deleting"
                print(f"{action} empty directory: {dirpath}")
                if not dry_run:
                    try:
                        os.rmdir(dirpath)
                        deleted_count += 1
                    except OSError as e:
                        print(f"Error deleting '{dirpath}': {e}", file=sys.stderr)
        except FileNotFoundError: # Directory might have been deleted by a previous step (e.g. parent of a deleted child)
            pass # Already gone, nothing to do
        except OSError as e:
            print(f"Error accessing '{dirpath}': {e}", file=sys.stderr)

    return deleted_count

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Digital Dust Bunny Sweeper: "
                    "Recursively cleans empty directories."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to start sweeping for dust bunnies (empty folders)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the cleaning process without actually deleting anything."
    )
    args = parser.parse_args()

    print(f"Starting the Nightly Digital Dust Bunny Sweeper in '{args.path}'...")
    if args.dry_run:
        print("Running in DRY-RUN mode. No files will be deleted.")

    deleted_count = clean_empty_dirs(args.path, args.dry_run)

    if deleted_count > 0:
        print(f"Sweeper finished. {'Would have deleted' if args.dry_run else 'Deleted'} {deleted_count} empty directories.")
    else:
        print("Sweeper finished. No empty directories found to clean.")

if __name__ == "__main__":
    main()
