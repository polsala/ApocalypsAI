import os
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def clean_empty_dirs(root_dir: str, dry_run: bool = False) -> list[str]:
    """
    Recursively finds and removes empty directories within a given root directory.

    Args:
        root_dir: The path to the directory to start cleaning from.
        dry_run: If True, only report what would be removed without actually deleting.

    Returns:
        A list of paths to directories that were (or would be) removed.
    """
    if not os.path.isdir(root_dir):
        logging.error(f"Error: Root directory '{root_dir}' does not exist or is not a directory.")
        return []

    removed_dirs = []
    # Walk from bottom-up (topdown=False) to ensure subdirectories are processed before parents.
    # This allows a parent directory to become empty and be removed if all its children are removed.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not dirnames and not filenames:
            # Directory is empty
            if os.path.abspath(dirpath) == os.path.abspath(root_dir):
                # Do not remove the root directory itself, even if it becomes empty
                continue

            if dry_run:
                logging.info(f"[DRY RUN] Would remove empty directory: {dirpath}")
            else:
                try:
                    os.rmdir(dirpath)
                    logging.info(f"Removed empty directory: {dirpath}")
                    removed_dirs.append(dirpath)
                except OSError as e:
                    logging.error(f"Failed to remove directory {dirpath}: {e}")
    return removed_dirs

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Digital Dust Bunny Sweeper: Recursively removes empty directories."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to start sweeping for empty directories."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the removal process without actually deleting any directories."
    )
    args = parser.parse_args()

    logging.info(f"Starting Digital Dust Bunny Sweeper for path: {args.path}")
    if args.dry_run:
        logging.info("Running in DRY RUN mode. No directories will be deleted.")

    removed_count = len(clean_empty_dirs(args.path, args.dry_run))

    if removed_count > 0:
        logging.info(f"Sweeping complete. {'Would have removed' if args.dry_run else 'Removed'} {removed_count} empty directories.")
    else:
        logging.info("Sweeping complete. No empty directories found to remove.")

if __name__ == "__main__":
    main()
