import os
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_dust(directory: Path, age_days: int, dry_run: bool = False):
    """
    Removes files in the specified directory that are older than the given age.

    Args:
        directory (Path): The path to the directory to clean.
        age_days (int): The age in days. Files older than this will be removed.
        dry_run (bool): If True, only report files to be deleted, do not delete.
    """
    if not directory.is_dir():
        logging.error(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return

    logging.info(f"Scanning directory: {directory} for files older than {age_days} days.")
    if dry_run:
        logging.info("DRY RUN mode: No files will be actually deleted.")

    current_time = datetime.now()
    threshold_time = current_time - timedelta(days=age_days)
    deleted_count = 0
    skipped_count = 0

    for item in directory.iterdir():
        if item.is_file():
            try:
                # Get last modification time of the file
                mtime_timestamp = item.stat().st_mtime
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < threshold_time:
                    if dry_run:
                        logging.info(f"[DRY RUN] Would delete: {item} (last modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                    else:
                        item.unlink()  # Delete the file
                        logging.info(f"Deleted: {item} (last modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                        deleted_count += 1
                else:
                    logging.debug(f"Keeping: {item} (last modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
                    skipped_count += 1
            except OSError as e:
                logging.warning(f"Could not process file {item}: {e}")
        elif item.is_dir():
            logging.debug(f"Skipping directory: {item}")
        else:
            logging.debug(f"Skipping non-file item: {item}")

    if dry_run:
        logging.info(f"Dry run complete. Would have deleted {deleted_count} files. Skipped {skipped_count} files.")
    else:
        logging.info(f"Cleanup complete. Deleted {deleted_count} files. Skipped {skipped_count} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Cleans up old files in a directory."
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="The path to the directory to clean."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be removed."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only report files to be deleted, do not delete."
    )

    args = parser.parse_args()

    target_directory = Path(args.directory)
    age_in_days = args.age
    is_dry_run = args.dry_run

    collect_dust(target_directory, age_in_days, is_dry_run)

if __name__ == "__main__":
    main()
