import os
import zipfile
import datetime
import argparse
import shutil

def _get_timestamp():
    """Helper to get a formatted timestamp."""
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def _create_zip_archive(source_path, archive_name, message=None):
    """Creates a zip archive of the source_path."""
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            if os.path.isfile(source_path):
                zf.write(source_path, os.path.basename(source_path))
            elif os.path.isdir(source_path):
                for root, _, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                        zf.write(file_path, arcname)
            else:
                raise FileNotFoundError(f"Source path not found: {source_path}")

            if message:
                zf.writestr('message.txt', message)
        return True
    except Exception as e:
        print(f"Error creating archive {archive_name}: {e}")
        return False

def create_echo(source_path, output_dir="echoes", message=None):
    """
    Creates a timestamped zip archive (echo) of the given source_path.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    item_name = os.path.basename(source_path)
    timestamp = _get_timestamp()
    archive_filename = f"echo-{timestamp}-{item_name}.zip"
    archive_path = os.path.join(output_dir, archive_filename)

    print(f"Creating echo for '{source_path}'...")
    if _create_zip_archive(source_path, archive_path, message):
        print(f"Echo created successfully: {archive_path}")
    else:
        print(f"Failed to create echo for '{source_path}'.")

def list_echoes(output_dir="echoes"):
    """
    Lists all echo archives in the specified output directory.
    """
    if not os.path.exists(output_dir):
        print(f"No echoes directory found at '{output_dir}'.")
        return

    echo_files = [f for f in os.listdir(output_dir) if f.startswith("echo-") and f.endswith(".zip")]
    if not echo_files:
        print(f"No echoes found in '{output_dir}'.")
        return

    print(f"Echoes in '{output_dir}':")
    for echo in sorted(echo_files):
        print(f"- {echo}")

def retrieve_echo(echo_archive_path, extract_dir=None):
    """
    Extracts the contents of a specific echo archive.
    """
    if not os.path.exists(echo_archive_path):
        print(f"Error: Echo archive '{echo_archive_path}' not found.")
        return

    if not zipfile.is_zipfile(echo_archive_path):
        print(f"Error: '{echo_archive_path}' is not a valid zip file.")
        return

    if extract_dir is None:
        # Default extract directory is a folder named after the zip file (without .zip)
        extract_dir = os.path.splitext(os.path.basename(echo_archive_path))[0]

    os.makedirs(extract_dir, exist_ok=True)

    print(f"Retrieving echo from '{echo_archive_path}' to '{extract_dir}'...")
    try:
        with zipfile.ZipFile(echo_archive_path, 'r') as zf:
            zf.extractall(extract_dir)
        print(f"Echo retrieved successfully to '{extract_dir}'.")
    except Exception as e:
        print(f"Error retrieving echo: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Echo Chamber: Bury your thoughts, retrieve your past."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new echo archive.")
    create_parser.add_argument("path", help="Path to the file or directory to archive.")
    create_parser.add_argument("--message", "-m", help="Optional message to include in the echo.")
    create_parser.add_argument("--output-dir", "-o", default="echoes",
                               help="Directory to store the echo archives. Defaults to 'echoes'.")

    # List command
    list_parser = subparsers.add_parser("list", help="List existing echo archives.")
    list_parser.add_argument("--output-dir", "-o", default="echoes",
                             help="Directory to list echoes from. Defaults to 'echoes'.")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve (extract) an echo archive.")
    retrieve_parser.add_argument("echo_archive_path", help="Path to the echo .zip file.")
    retrieve_parser.add_argument("--extract-dir", "-e",
                                 help="Directory to extract the echo contents to. Defaults to a new folder named after the echo.")

    args = parser.parse_args()

    if args.command == "create":
        create_echo(args.path, args.output_dir, args.message)
    elif args.command == "list":
        list_echoes(args.output_dir)
    elif args.command == "retrieve":
        retrieve_echo(args.echo_archive_path, args.extract_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
