import os
import sys
import argparse
import datetime
import re

def sanitize_filename(filename):
    """Sanitizes a string to be a valid filename component."""
    # Remove invalid characters (e.g., /?<>\:*|")
    sanitized = re.sub(r'[\\/:*?"<>|]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Limit length to avoid filesystem issues, though timestamp prefix helps
    return sanitized[:100] # Arbitrary limit

def rename_files_in_directory(
    directory: str,
    use_creation_time: bool = False,
    dry_run: bool = False,
    keep_original_name: bool = False
):
    """Renames files in a directory based on their timestamp.

    Args:
        directory (str): The path to the directory.
        use_creation_time (bool): If True, use creation time; otherwise, modification time.
        dry_run (bool): If True, only print actions, don't rename.
        keep_original_name (bool): If True, append original name to timestamp.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    print(f"Scanning directory: {directory}")
    print(f"Using {'creation' if use_creation_time else 'modification'} time.")
    if dry_run:
        print("DRY RUN: No files will be actually renamed.")

    renamed_count = 0
    timestamp_counts = {}

    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        if os.path.isfile(old_path):
            try:
                # Get timestamp (creation or modification)
                timestamp_float = os.path.getctime(old_path) if use_creation_time else os.path.getmtime(old_path)
                dt_object = datetime.datetime.fromtimestamp(timestamp_float)
                timestamp_str = dt_object.strftime('%Y%m%d_%H%M%S')

                # Handle potential conflicts for the same timestamp
                base_new_name_prefix = timestamp_str
                if base_new_name_prefix not in timestamp_counts:
                    timestamp_counts[base_new_name_prefix] = 0
                timestamp_counts[base_new_name_prefix] += 1

                counter_suffix = ''
                if timestamp_counts[base_new_name_prefix] > 1:
                    counter_suffix = f"_{timestamp_counts[base_new_name_prefix]:02d}"

                # Determine new filename
                name, ext = os.path.splitext(filename)
                ext = ext.lower() # Standardize extension case

                if keep_original_name:
                    sanitized_original_name = sanitize_filename(name)
                    new_filename = f"{timestamp_str}{counter_suffix}_{sanitized_original_name}{ext}"
                else:
                    new_filename = f"{timestamp_str}{counter_suffix}{ext}"

                new_path = os.path.join(directory, new_filename)

                if old_path == new_path:
                    print(f"  Skipping '{filename}': Already correctly named or no change needed.")
                    continue

                if dry_run:
                    print(f"  Would rename '{filename}' -> '{new_filename}'")
                else:
                    # Check if target filename already exists (e.g., if original name was very similar)
                    if os.path.exists(new_path):
                        print(f"  Warning: Target '{new_filename}' already exists. Skipping '{filename}'.")
                        continue
                    os.rename(old_path, new_path)
                    print(f"  Renamed '{filename}' -> '{new_filename}'")
                    renamed_count += 1

            except OSError as e:
                print(f"  Error processing '{filename}': {e}")
            except Exception as e:
                print(f"  Unexpected error with '{filename}': {e}")

    if not dry_run:
        print(f"\nFinished. Renamed {renamed_count} files.")
    else:
        print("\nDry run finished. No files were actually renamed.")

def main():
    parser = argparse.ArgumentParser(
        description="Rename files in a directory based on their timestamp."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory containing the files to be renamed."
    )
    parser.add_argument(
        "--use-creation-time",
        action="store_true",
        help="Use the file's creation timestamp instead of the last modification timestamp."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run. The utility will print the proposed renames without modifying any files."
    )
    parser.add_argument(
        "--keep-original-name",
        action="store_true",
        help="Append a sanitized version of the original filename after the timestamp."
    )

    args = parser.parse_args()

    rename_files_in_directory(
        args.directory,
        args.use_creation_time,
        args.dry_run,
        args.keep_original_name
    )

if __name__ == "__main__":
    main()
