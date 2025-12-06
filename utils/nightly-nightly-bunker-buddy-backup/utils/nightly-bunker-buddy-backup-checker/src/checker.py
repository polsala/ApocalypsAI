import argparse
import os
import sys
from datetime import datetime

def check_backup_status(source_path: str, backup_base_path: str) -> tuple[str, str]:
    """
    Checks the backup status of a single source item (file or directory).
    Returns a tuple of (status, message).
    """
    if not os.path.exists(source_path):
        return "SOURCE MISSING", f"Source '{source_path}' does not exist. Cannot check backup."

    # Determine the corresponding path in the backup bunker
    source_name = os.path.basename(source_path)
    backup_path = os.path.join(backup_base_path, source_name)

    if not os.path.exists(backup_path):
        return "MISSING IN BUNKER", f"'{source_name}' is missing in the bunker at '{backup_base_path}'."

    # Compare modification times
    source_mtime = os.path.getmtime(source_path)
    backup_mtime = os.path.getmtime(backup_path)

    if source_mtime > backup_mtime:
        source_dt = datetime.fromtimestamp(source_mtime).strftime('%Y-%m-%d %H:%M:%S')
        backup_dt = datetime.fromtimestamp(backup_mtime).strftime('%Y-%m-%d %H:%M:%S')
        return "OUTDATED", f"'{source_name}' in bunker is older (last modified: {backup_dt}) than source (last modified: {source_dt})."
    else:
        return "UP-TO-DATE", f"'{source_name}' in bunker is up-to-date (last modified: {datetime.fromtimestamp(backup_mtime).strftime('%Y-%m-%d %H:%M:%S')})."

def main():
    parser = argparse.ArgumentParser(
        description="Bunker Buddy Backup Checker: Ensure your critical files are backed up."
    )
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Path to a critical file or directory. Can be specified multiple times."
    )
    parser.add_argument(
        "--backup",
        required=True,
        help="Path to your backup 'bunker' directory."
    )

    args = parser.parse_args()

    backup_bunker_path = args.backup
    if not os.path.isdir(backup_bunker_path):
        print(f"Error: The specified bunker directory '{backup_bunker_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    print(f"\n--- Bunker Buddy Backup Report for '{backup_bunker_path}' ---")
    all_ok = True
    for source_item in args.source:
        status, message = check_backup_status(source_item, backup_bunker_path)
        print(f"[{status.ljust(15)}] {message}")
        if status != "UP-TO-DATE": # If any item is not up-to-date, the overall status is not 'all_ok'
            all_ok = False

    print("--------------------------------------------------")
    if all_ok:
        print("All critical supplies are accounted for and up-to-date in the bunker! Good job, survivor.")
        sys.exit(0)
    else:
        print("Attention, survivor! Some critical supplies need your immediate attention!")
        sys.exit(1)

if __name__ == "__main__":
    main()
