import os
import shutil
import argparse
from datetime import datetime, timedelta

def find_and_manage_forgotten_files(
    target_dir: str,
    age_days: int,
    quarantine_dir: str = None,
    report_only: bool = False
) -> dict:
    """
    Scans a directory for files older than a specified age and either reports them
    or moves them to a quarantine directory.

    Args:
        target_dir: The root directory to scan.
        age_days: The minimum age in days for a file to be considered forgotten.
        quarantine_dir: Optional directory to move forgotten files to.
        report_only: If True, only reports files, does not move them.

    Returns:
        A dictionary containing lists of 'found_files', 'quarantined_files', and 'errors'.
    """
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return {'found_files': [], 'quarantined_files': [], 'errors': [f"Target directory '{target_dir}' not found."]}

    if quarantine_dir and not report_only:
        os.makedirs(quarantine_dir, exist_ok=True)
        if not os.path.isdir(quarantine_dir):
            print(f"Error: Could not create or access quarantine directory '{quarantine_dir}'.")
            return {'found_files': [], 'quarantined_files': [], 'errors': [f"Quarantine directory '{quarantine_dir}' inaccessible."]}

    now = datetime.now()
    threshold_date = now - timedelta(days=age_days)

    found_files = []
    quarantined_files = []
    errors = []

    print(f"🕵️‍♀️ Scanning '{target_dir}' for files older than {age_days} days (modified before {threshold_date.strftime('%Y-%m-%d %H:%M:%S')})...")

    for root, _, files in os.walk(target_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Use modification time (mtime) as it's more consistently updated than access time (atime)
                # and reflects when the file's content last changed.
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < threshold_date:
                    found_files.append(file_path)
                    print(f"  Found forgotten file: {file_path} (Modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")

                    if quarantine_dir and not report_only:
                        try:
                            relative_path = os.path.relpath(file_path, target_dir)
                            dest_path = os.path.join(quarantine_dir, relative_path)
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            shutil.move(file_path, dest_path)
                            quarantined_files.append(file_path)
                            print(f"    -> Moved to quarantine: {dest_path}")
                        except Exception as e:
                            errors.append(f"Failed to move '{file_path}': {e}")
                            print(f"    -> Error moving file: {e}")

            except FileNotFoundError:
                errors.append(f"File not found during scan (might have been deleted): {file_path}")
            except Exception as e:
                errors.append(f"Error processing '{file_path}': {e}")

    print("\n--- Scan Summary ---")
    if found_files:
        print(f"Total forgotten files found: {len(found_files)}")
        if quarantine_dir and not report_only:
            print(f"Total files quarantined: {len(quarantined_files)}")
            print(f"Files still in place (due to errors or report-only mode): {len(found_files) - len(quarantined_files)}")
        else:
            print("No files were moved (report-only mode or no quarantine directory specified).")
    else:
        print("No forgotten files found. Your digital space is sparkling clean! ✨")

    if errors:
        print(f"\n--- Errors encountered: {len(errors)} ---")
        for err in errors:
            print(f"  - {err}")

    return {
        'found_files': found_files,
        'quarantined_files': quarantined_files,
        'errors': errors
    }

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Forgotten File Finder: Unearths and manages old files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for forgotten files."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="The minimum age in days for a file to be considered 'forgotten'."
    )
    parser.add_argument(
        "--quarantine",
        type=str,
        default=None,
        help="Optional directory to move forgotten files to. Will be created if it doesn't exist."
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="If set, the utility will only report the forgotten files and will not move them."
    )

    args = parser.parse_args()

    find_and_manage_forgotten_files(
        target_dir=args.path,
        age_days=args.age,
        quarantine_dir=args.quarantine,
        report_only=args.report_only
    )

if __name__ == "__main__":
    main()
