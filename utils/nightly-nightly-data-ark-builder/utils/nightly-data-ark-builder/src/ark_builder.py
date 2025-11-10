import argparse
import os
import zipfile
import datetime
import sys

def build_ark(source_paths, output_zip_path):
    """
    Builds a "data ark" by zipping specified source files and directories.
    Includes a manifest of all archived items.
    
    Args:
        source_paths (list): A list of paths to files or directories to archive.
        output_zip_path (str): The path where the output ZIP file will be created.

    Returns:
        list: A list of items (their arcnames) successfully added to the zip file.

    Raises:
        ValueError: If no source paths are provided or an unsupported path type is given.
        FileNotFoundError: If any of the source paths do not exist.
    """
    if not source_paths:
        raise ValueError("No source paths provided to archive.")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_zip_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    archived_items = []
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for source_path in source_paths:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source path '{source_path}' does not exist.")

            if os.path.isfile(source_path):
                arcname = os.path.basename(source_path)
                zf.write(source_path, arcname=arcname)
                archived_items.append(arcname)
            elif os.path.isdir(source_path):
                # Walk through the directory and add all files
                # Calculate arcname relative to the *parent* of the source_path
                # to ensure the source directory itself is the top-level entry in the zip.
                # Example: source_path = /tmp/my_data
                #          file_path = /tmp/my_data/docs/report.txt
                #          rel_path_from_parent = my_data/docs/report.txt
                for dirpath, dirnames, filenames in os.walk(source_path):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                        zf.write(file_path, arcname=arcname)
                        archived_items.append(arcname)
            else:
                # Handle symlinks, pipes, etc. - for simplicity, raise an error
                raise ValueError(f"Unsupported source path type: '{source_path}' (must be file or directory).")

        # Create manifest
        manifest_content = f"ApocalypsAI Data Ark Manifest\n" \
                           f"Created: {datetime.datetime.now().isoformat()}\n" \
                           f"Source Paths: {', '.join(source_paths)}\n\n" \
                           f"Archived Items:\n"
        for item in sorted(archived_items):
            manifest_content += f"- {item}\n"

        zf.writestr('MANIFEST.txt', manifest_content)
        archived_items.append('MANIFEST.txt') # Add manifest to the list for verification

    return archived_items # Return list of items added to the zip

def main():
    parser = argparse.ArgumentParser(
        description="Builds a 'Data Ark' (ZIP archive) of your essential files for post-apocalyptic survival."
    )
    parser.add_argument(
        '--source',
        nargs='+',
        required=True,
        help="One or more paths to files or directories to include in the ark."
    )
    parser.add_argument(
        '--output',
        required=True,
        help="Path to the output ZIP file (e.g., 'my_ark.zip')."
    )

    args = parser.parse_args()

    try:
        print(f"Building Data Ark '{args.output}' from sources: {', '.join(args.source)}...")
        archived_items = build_ark(args.source, args.output)
        print(f"Data Ark '{args.output}' successfully created with {len(archived_items)} items.")
        print("Archived items:")
        for item in sorted(archived_items): # Sort for consistent output
            print(f"  - {item}")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error building Data Ark: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
