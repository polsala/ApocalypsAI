import argparse
import os
import zipfile
import datetime

def create_apocalypse_package(source_paths: list[str], output_dir: str) -> str:
    """
    Packages specified files and directories into a timestamped ZIP archive.

    Args:
        source_paths: A list of paths to files or directories to include.
        output_dir: The directory where the ZIP archive will be created.

    Returns:
        The full path to the created ZIP archive.

    Raises:
        FileNotFoundError: If any source path does not exist.
        IOError: If there's an issue creating the ZIP file or adding contents.
    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"apocalypse_prep_{timestamp}.zip"
    archive_path = os.path.join(output_dir, archive_name)

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for source_path in source_paths:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source path not found: {source_path}")

            if os.path.isfile(source_path):
                zf.write(source_path, os.path.basename(source_path))
            elif os.path.isdir(source_path):
                # Walk through the directory and add all files
                for root, _, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate relative path inside the zip to preserve directory structure
                        # If source_path is /a/b/my_dir and file_path is /a/b/my_dir/c/d.txt,
                        # then os.path.dirname(source_path) is /a/b.
                        # os.path.relpath(file_path, /a/b) will be my_dir/c/d.txt
                        arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                        zf.write(file_path, arcname)
            else:
                print(f"Warning: Skipping unsupported path type: {source_path}")

    return archive_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Package critical files into a timestamped ZIP archive."
    )
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Path to a file or directory to include. Can be specified multiple times.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory where the ZIP archive will be created.",
    )

    args = parser.parse_args()

    try:
        created_archive = create_apocalypse_package(args.source, args.output)
        print(f"Apocalypse prep package created: {created_archive}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except IOError as e:
        print(f"Error creating archive: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
