import os
import zipfile
import datetime
import argparse
import sys

def create_archive(source_dir: str, output_dir: str, archive_name_prefix: str = "echo-chamber-snapshot") -> str:
    """
    Creates a timestamped zip archive of the specified source directory.

    Args:
        source_dir: The path to the directory to be archived.
        output_dir: The path where the archive will be saved.
        archive_name_prefix: A prefix for the archive filename.

    Returns:
        The full path to the created archive file.

    Raises:
        FileNotFoundError: If the source directory does not exist.
        IOError: If there's an issue creating the output directory or the zip file.
    """
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for the archive name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_filename = f"{archive_name_prefix}_{timestamp}.zip"
    archive_path = os.path.join(output_dir, archive_filename)

    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate arcname to store files relative to source_dir
                    arcname = os.path.relpath(file_path, source_dir)
                    zf.write(file_path, arcname)
        return archive_path
    except Exception as e:
        raise IOError(f"Failed to create archive '{archive_path}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Temporal Echo Chamber: Create timestamped zip archives of directories."
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="The path to the directory to be archived."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="The path to the directory where the archive will be saved."
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="echo-chamber-snapshot",
        help="A prefix for the archive filename (default: 'echo-chamber-snapshot')."
    )

    args = parser.parse_args()

    try:
        archive_path = create_archive(args.source, args.output, args.prefix)
        print(f"Successfully created archive: {archive_path}")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
