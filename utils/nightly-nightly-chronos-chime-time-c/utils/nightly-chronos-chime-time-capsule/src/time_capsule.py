import os
import zipfile
import datetime
import argparse

def create_capsule(source_dir: str, output_dir: str, capsule_name_prefix: str = "chronos_chime") -> str:
    """
    Creates a timestamped ZIP archive (time capsule) of the specified source directory.

    Args:
        source_dir: The path to the directory to be archived.
        output_dir: The directory where the time capsule (ZIP file) will be saved.
        capsule_name_prefix: A prefix for the time capsule filename.

    Returns:
        The full path to the created time capsule file, or an empty string if creation failed.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return ""
    if not os.path.isdir(source_dir):
        print(f"Error: Source path '{source_dir}' is not a directory.")
        return ""

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    capsule_filename = f"{capsule_name_prefix}_{timestamp}.zip"
    capsule_path = os.path.join(output_dir, capsule_filename)

    try:
        with zipfile.ZipFile(capsule_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Arcname is the path inside the zip file, relative to the source_dir
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        print(f"Time capsule created successfully at: {capsule_path}")
        return capsule_path
    except Exception as e:
        print(f"Error creating time capsule: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="Create a timestamped digital time capsule (ZIP archive) of a directory."
    )
    parser.add_argument(
        "--source",
        required=True,
        help="The path to the directory to be archived."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="The directory where the time capsule (ZIP file) will be saved."
    )
    parser.add_argument(
        "--prefix",
        default="chronos_chime",
        help="A custom prefix for the capsule filename (default: chronos_chime)."
    )

    args = parser.parse_args()

    create_capsule(args.source, args.output, args.prefix)


if __name__ == "__main__":
    main()
