import os
import argparse
import datetime
import sys

def get_modification_date(filepath):
    """
    Retrieves the last modification date of a file.
    Returns date in YYYY-MM-DD format.
    """
    timestamp = os.path.getmtime(filepath)
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d')

def is_already_renamed(filename, date_prefix):
    """
    Checks if a file already has the expected date prefix.
    """
    return filename.startswith(f"{date_prefix}_")

def rename_files_in_directory(directory_path, dry_run=False):
    """
    Scans a directory and renames files by prepending their modification date.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.", file=sys.stderr)
        return 1

    print(f"Scanning directory: {directory_path}")
    if dry_run:
        print("--- DRY RUN MODE --- No files will be actually renamed.")

    renamed_count = 0
    skipped_count = 0
    error_count = 0

    try:
        for filename in os.listdir(directory_path):
            old_filepath = os.path.join(directory_path, filename)

            if os.path.isdir(old_filepath):
                print(f"Skipping directory: {filename}")
                continue

            try:
                mod_date = get_modification_date(old_filepath)
                if is_already_renamed(filename, mod_date):
                    print(f"Skipping '{filename}': Already has date prefix '{mod_date}_'.")
                    skipped_count += 1
                    continue

                new_filename = f"{mod_date}_{filename}"
                new_filepath = os.path.join(directory_path, new_filename)

                if dry_run:
                    print(f"[DRY RUN] Would rename: '{filename}' -> '{new_filename}'")
                else:
                    os.rename(old_filepath, new_filepath)
                    print(f"Renamed: '{filename}' -> '{new_filename}'")
                    renamed_count += 1

            except OSError as e:
                print(f"Error processing file '{filename}': {e}", file=sys.stderr)
                error_count += 1
            except Exception as e:
                print(f"Unexpected error with file '{filename}': {e}", file=sys.stderr)
                error_count += 1

    except OSError as e:
        print(f"Error listing directory '{directory_path}': {e}", file=sys.stderr)
        return 1

    print("\n--- Summary ---")
    print(f"Files renamed: {renamed_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Files with errors: {error_count}")

    return 0 if error_count == 0 else 1

def main():
    parser = argparse.ArgumentParser(
        description="Rename files by prepending their last modification date (YYYY-MM-DD)."
    )
    parser.add_argument(
        "--directory",
        "-d",
        required=True,
        help="The path to the directory containing files to be renamed."
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="If set, only print what would be done without making actual changes."
    )

    args = parser.parse_args()
    sys.exit(rename_files_in_directory(args.directory, args.dry_run))

if __name__ == "__main__":
    main()
