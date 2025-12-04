import os
import datetime
import argparse

def format_bytes(size):
    """Formats a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def generate_manifest(directory: str, output_file: str, file_extensions: list = None):
    """
    Generates a markdown manifest of files in the given directory.

    Args:
        directory (str): The path to the directory to scan.
        output_file (str): The path to the output markdown file.
        file_extensions (list, optional): A list of file extensions to include (e.g., ['.txt', '.log']).
                                          If None, all files are included.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")

    manifest_content = [
        f"# Scavenger's Manifest for '{os.path.basename(directory)}'",
        f"Generated on: {datetime.datetime.now().isoformat()}",
        "",
        "| File Path | Size | Last Modified |",
        "|---|---|---|",
    ]

    for root, _, files in os.walk(directory):
        for file in files:
            if file_extensions and not any(file.endswith(ext) for ext in file_extensions):
                continue

            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                last_modified = datetime.datetime.fromtimestamp(mtime).isoformat()
                relative_path = os.path.relpath(file_path, directory)
                manifest_content.append(
                    f"| `{relative_path}` | {format_bytes(size)} | {last_modified} |"
                )
            except OSError as e:
                manifest_content.append(f"| `{file_path}` | ERROR: {e} | ERROR |")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(manifest_content))

    print(f"Manifest generated successfully at: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate a markdown manifest of files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="scavenger_manifest.md",
        help="The path to the output markdown file. Defaults to 'scavenger_manifest.md'."
    )
    parser.add_argument(
        "-e", "--extensions",
        nargs='*',
        help="Optional list of file extensions to include (e.g., .txt .log). "
             "If not provided, all files are included."
    )

    args = parser.parse_args()

    # Ensure extensions start with a dot if provided
    if args.extensions:
        args.extensions = [ext if ext.startswith('.') else f".{ext}" for ext in args.extensions]

    try:
        generate_manifest(args.directory, args.output, args.extensions)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
