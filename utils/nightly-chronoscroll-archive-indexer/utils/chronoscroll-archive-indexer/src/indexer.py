import os
import json
import argparse
from datetime import datetime, timezone

def get_file_metadata(filepath):
    """
    Extracts metadata for a given file.
    """
    stat = os.stat(filepath)
    return {
        "name": os.path.basename(filepath),
        "size_bytes": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }

def scan_directory(path):
    """
    Scans a directory and collects metadata for all files.
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    files_data = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            try:
                files_data.append(get_file_metadata(filepath))
            except OSError as e:
                print(f"Warning: Could not get metadata for {filepath}: {e}")
    return files_data

def format_as_markdown(scan_path, files_data):
    """
    Formats the collected file data as a Markdown string.
    """
    output = [
        f"# Chronoscroll Archive Index - {scan_path}",
        f"\n**Scan Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## Files Found: {len(files_data)}\n"
    ]

    for file_info in files_data:
        output.append(f"- **{file_info['name']}**")
        output.append(f"  - Size: {file_info['size_bytes']} bytes")
        output.append(f"  - Last Modified: {datetime.fromisoformat(file_info['last_modified']).strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(output)

def format_as_json(scan_path, files_data):
    """
    Formats the collected file data as a JSON string.
    """
    data = {
        "scan_date": datetime.now(timezone.utc).isoformat(),
        "scanned_path": scan_path,
        "files_count": len(files_data),
        "files": files_data
    }
    return json.dumps(data, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="Chronoscroll Archive Indexer: Catalog 'ancient data fragments'."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for files."
    )
    parser.add_argument(
        "--output-format",
        type=str,
        default="markdown",
        choices=["markdown", "json"],
        help="The desired output format (markdown or json)."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Optional: If provided, output will be written to this file. Otherwise, prints to stdout."
    )

    args = parser.parse_args()

    try:
        files_data = scan_directory(args.path)

        if args.output_format == "markdown":
            output_content = format_as_markdown(args.path, files_data)
        else: # json
            output_content = format_as_json(args.path, files_data)

        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"Index successfully written to {args.output_file}")
        else:
            print(output_content)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
