import os
import argparse
from datetime import datetime
from collections import defaultdict

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(os.path.floor(os.path.log(size_bytes, 1024)))
    p = os.path.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def generate_manifest(directory_path, output_file=None):
    """
    Scans a directory, categorizes files by extension, and generates a summary manifest.

    Args:
        directory_path (str): The path to the directory to scan.
        output_file (str, optional): Path to a file to write the manifest to. If None, prints to stdout.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return

    file_data = defaultdict(lambda: {'count': 0, 'total_size': 0, 'mod_times': []})
    total_files = 0
    total_overall_size = 0

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                mod_time = os.path.getmtime(file_path)
                extension = os.path.splitext(file_name)[1].lower() or "(no extension)"

                file_data[extension]['count'] += 1
                file_data[extension]['total_size'] += size
                file_data[extension]['mod_times'].append(mod_time)
                total_files += 1
                total_overall_size += size
            except OSError as e:
                # Skip files that can't be accessed (e.g., broken symlinks, permission issues)
                print(f"Warning: Could not access '{file_path}': {e}")
                continue

    manifest_lines = []
    manifest_lines.append(f"Scavenger's Manifest for: {directory_path}")
    manifest_lines.append(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    manifest_lines.append(f"\nTotal Files Scanned: {total_files}")
    manifest_lines.append(f"Total Size: {format_size(total_overall_size)}")
    manifest_lines.append(f"\n--- File Type Summary ---")

    for ext in sorted(file_data.keys()):
        data = file_data[ext]
        manifest_lines.append(f"{ext}:")
        manifest_lines.append(f"  Count: {data['count']}")
        manifest_lines.append(f"  Total Size: {format_size(data['total_size'])}")
        if data['mod_times']:
            oldest_mod = datetime.fromtimestamp(min(data['mod_times'])).strftime('%Y-%m-%d %H:%M:%S')
            newest_mod = datetime.fromtimestamp(max(data['mod_times'])).strftime('%Y-%m-%d %H:%M:%S')
            manifest_lines.append(f"  Last Modified (oldest): {oldest_mod}")
            manifest_lines.append(f"  Last Modified (newest): {newest_mod}")
        manifest_lines.append("") # Blank line for spacing

    manifest_lines.append(f"--- End Manifest ---")

    manifest_content = "\n".join(manifest_lines)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(manifest_content)
            print(f"Manifest successfully written to '{output_file}'")
        except IOError as e:
            print(f"Error: Could not write manifest to '{output_file}': {e}")
    else:
        print(manifest_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scans a directory and generates a file manifest."
    )
    parser.add_argument("directory", help="The directory to scan.")
    parser.add_argument("--output", help="Optional: path to an output file for the manifest.")
    args = parser.parse_args()

    generate_manifest(args.directory, args.output)
