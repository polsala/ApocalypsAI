import os
import sys
import fnmatch
from datetime import datetime

def get_file_metadata(filepath):
    """Retrieves size and last modification time for a given file."""
    try:
        size = os.path.getsize(filepath)
        mtime = os.path.getmtime(filepath)
        last_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        return size, last_modified
    except OSError:
        return None, None

def scan_directory(root_dir, include_patterns):
    """
    Scans a directory for files matching include_patterns and gathers their metadata.
    Returns a list of dictionaries, each containing 'path', 'size', 'mtime'.
    """
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"Directory not found: {root_dir}")

    manifest_entries = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            
            # Check if the file matches any of the include patterns
            if any(fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(relative_path, pattern) for pattern in include_patterns):
                full_path = os.path.join(dirpath, filename)
                size, mtime = get_file_metadata(full_path)
                if size is not None:
                    manifest_entries.append({
                        'path': relative_path,
                        'size': size,
                        'mtime': mtime
                    })
    return manifest_entries

def generate_markdown_manifest(root_dir, manifest_entries):
    """Generates a Markdown formatted string from manifest entries."""
    header = f"# Mutant Manifest for {os.path.abspath(root_dir)}\n\n"
    table_header = "| File Path | Size (bytes) | Last Modified |\n"
    table_separator = "|---|---|---|\n"

    table_rows = []
    for entry in sorted(manifest_entries, key=lambda x: x['path']):
        table_rows.append(f"| {entry['path']} | {entry['size']} | {entry['mtime']} |")

    return header + table_header + table_separator + "\n".join(table_rows) + "\n"

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/manifest_maker.py <directory_to_scan> [pattern1] [pattern2] ...")
        sys.exit(1)

    root_dir = sys.argv[1]
    include_patterns = sys.argv[2:] if len(sys.argv) > 2 else ["*"] # Default to all files if no patterns

    try:
        manifest_entries = scan_directory(root_dir, include_patterns)
        markdown_output = generate_markdown_manifest(root_dir, manifest_entries)
        print(markdown_output)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
