import argparse
import os
import shutil
from datetime import datetime

def create_archive(output_dir: str, files_to_archive: list[str]):
    """
    Archives specified files and directories into a timestamped folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"archive_{timestamp}"
    archive_path = os.path.join(output_dir, archive_name)

    os.makedirs(archive_path, exist_ok=True)
    print(f"Created archive directory: {archive_path}")

    for item_path in files_to_archive:
        if not os.path.exists(item_path):
            print(f"Warning: Path not found - {item_path}. Skipping.")
            continue

        destination_path = os.path.join(archive_path, os.path.basename(item_path))

        if os.path.isfile(item_path):
            shutil.copy2(item_path, destination_path)
            print(f"Archived file: {item_path} -> {destination_path}")
        elif os.path.isdir(item_path):
            shutil.copytree(item_path, destination_path, dirs_exist_ok=True)
            print(f"Archived directory: {item_path} -> {destination_path}")
        else:
            print(f"Warning: Unknown item type for {item_path}. Skipping.")

    print(f"Archiving complete for {len(files_to_archive)} items.")
    return archive_path

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Artifact Archiver: Preserves critical project files into a timestamped archive."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="The base directory where archives will be stored."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="One or more paths to files or directories to be archived."
    )

    args = parser.parse_args()

    create_archive(args.output_dir, args.files)

if __name__ == "__main__":
    main()
