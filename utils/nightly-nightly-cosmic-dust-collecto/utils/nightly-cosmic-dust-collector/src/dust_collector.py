import os
import shutil
import argparse
import datetime

def collect_dust(directory: str, age_days: int, extensions: list[str], dry_run: bool = False) -> list[str]:
    """
    Scans a directory for files older than a specified age and moves them to an 'archive' subdirectory.

    Args:
        directory (str): The root directory to scan.
        age_days (int): The age threshold in days. Files older than this will be archived.
        extensions (list[str]): A list of file extensions (without leading dot) to target.
        dry_run (bool): If True, only report actions without performing them.

    Returns:
        list[str]: A list of paths to files that were moved (or would have been moved in dry-run mode).
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return []

    archive_dir = os.path.join(directory, "archive")
    if not os.path.exists(archive_dir):
        if not dry_run:
            os.makedirs(archive_dir)
            print(f"Created archive directory: {archive_dir}")
        else:
            print(f"Would create archive directory: {archive_dir}")

    now = datetime.datetime.now()
    threshold_time = now - datetime.timedelta(days=age_days)
    moved_files = []

    print(f"Scanning '{directory}' for files older than {age_days} days with extensions: {', '.join(extensions)}")

    for root, _, files in os.walk(directory):
        # Skip the archive directory itself to prevent infinite loops or archiving already archived files
        if root.startswith(archive_dir):
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            file_extension = os.path.splitext(filename)[1].lstrip('.')

            if file_extension in extensions:
                try:
                    mod_timestamp = os.path.getmtime(file_path)
                    mod_datetime = datetime.datetime.fromtimestamp(mod_timestamp)

                    if mod_datetime < threshold_time:
                        # Calculate relative path to maintain directory structure in archive
                        relative_path = os.path.relpath(file_path, directory)
                        destination_path = os.path.join(archive_dir, relative_path)

                        # Ensure subdirectories in archive_dir exist for the file's destination
                        dest_subdir = os.path.dirname(destination_path)
                        if not os.path.exists(dest_subdir):
                            if not dry_run:
                                os.makedirs(dest_subdir)
                                print(f"Created archive subdirectory: {dest_subdir}")
                            else:
                                print(f"Would create archive subdirectory: {dest_subdir}")

                        if not dry_run:
                            shutil.move(file_path, destination_path)
                            print(f"Moved: {relative_path} -> archive/{relative_path}")
                        else:
                            print(f"Would move: {relative_path} -> archive/{relative_path}")
                        moved_files.append(file_path)
                except OSError as e:
                    print(f"Warning: Could not access file {file_path}: {e}")

    if not moved_files:
        print("No cosmic dust found to collect.")
    else:
        print(f"Collected {len(moved_files)} pieces of cosmic dust.")

    return moved_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collects old files of specified types and moves them to an 'archive' subdirectory."
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="The root directory to scan for old files."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="The age threshold in days. Files older than this will be archived."
    )
    parser.add_argument(
        "--extensions",
        nargs='+',
        required=True,
        help="A space-separated list of file extensions (without the leading dot) to target."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If specified, the utility will only report what *would* be moved, without actually moving any files."
    )

    args = parser.parse_args()

    collect_dust(args.directory, args.age, args.extensions, args.dry_run)
