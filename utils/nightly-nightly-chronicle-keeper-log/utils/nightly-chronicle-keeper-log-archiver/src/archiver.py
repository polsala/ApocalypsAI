import os
import shutil
import argparse
from datetime import datetime

def archive_logs(source_dir: str, archive_dir: str, delete_originals: bool = False):
    """
    Archives log files from a source directory into a single timestamped file
    in an archive directory. Optionally deletes original files.

    Args:
        source_dir (str): The path to the directory containing log files.
        archive_dir (str): The path to the directory where the archive will be saved.
        delete_originals (bool): If True, original log files will be deleted after archiving.
    """
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return False

    os.makedirs(archive_dir, exist_ok=True)

    log_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and f.endswith(('.log', '.txt'))]

    if not log_files:
        print(f"No log files (.log, .txt) found in '{source_dir}' to archive.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_filename = f"chronicle_archive_{timestamp}.log"
    archive_filepath = os.path.join(archive_dir, archive_filename)

    print(f"Archiving {len(log_files)} files from '{source_dir}' to '{archive_filepath}'...")

    try:
        with open(archive_filepath, 'w', encoding='utf-8') as outfile:
            for log_file in sorted(log_files): # Sort for deterministic output
                filepath = os.path.join(source_dir, log_file)
                outfile.write(f"--- Start of {log_file} ---\n")
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                    outfile.write(infile.read())
                outfile.write(f"--- End of {log_file} ---\n\n")
        
        print(f"Successfully created archive: '{archive_filepath}'")

        if delete_originals:
            for log_file in log_files:
                filepath = os.path.join(source_dir, log_file)
                os.remove(filepath)
                print(f"Deleted original file: '{filepath}'")
        
        return True

    except Exception as e:
        print(f"An error occurred during archiving: {e}")
        # Clean up partially created archive if an error occurs
        if os.path.exists(archive_filepath):
            os.remove(archive_filepath)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper Log Archiver: Consolidates log files into a timestamped archive."
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="The directory containing the log files to be archived."
    )
    parser.add_argument(
        "--archive",
        type=str,
        required=True,
        help="The directory where the consolidated archive file will be saved."
    )
    parser.add_argument(
        "--delete-originals",
        action="store_true",
        help="If provided, original log files in the source directory will be deleted after archiving."
    )

    args = parser.parse_args()

    success = archive_logs(args.source, args.archive, args.delete_originals)
    if not success:
        exit(1) # Indicate failure

if __name__ == "__main__":
    main()
