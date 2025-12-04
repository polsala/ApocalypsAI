import os
import argparse
import fnmatch

def generate_manifest(directory: str, patterns: list[str], output_file: str, snippet_length: int = 0):
    """
    Scans a directory for files matching patterns and generates a markdown manifest.

    Args:
        directory (str): The root directory to scan.
        patterns (list[str]): List of glob-style patterns to match files. If empty, all files are included.
        output_file (str): Path to the output markdown manifest file.
        snippet_length (int): Number of characters to include as a content snippet (0 for no snippet).
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    manifest_entries = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Check if file matches any pattern, or if no patterns are specified
            if not patterns or any(fnmatch.fnmatch(filename, p) for p in patterns):
                try:
                    size = os.path.getsize(filepath)
                    snippet = ""
                    if snippet_length > 0:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            snippet = f.read(snippet_length)
                            if len(snippet) == snippet_length: # Indicate truncation
                                snippet += "..."

                    manifest_entries.append({
                        "path": filepath,
                        "size": size,
                        "snippet": snippet
                    })
                except OSError as e:
                    print(f"Warning: Could not process {filepath}: {e}")

    manifest_content = "# Scavenger's Manifest\n\n"
    if not manifest_entries:
        manifest_content += f"No matching files found in '{directory}' with patterns {patterns if patterns else 'all files'}.\n"
    else:
        manifest_content += "| Path | Size (bytes) | Snippet |\n"
        manifest_content += "| :--- | :----------: | :------ |\n"
        for entry in manifest_entries:
            # Escape markdown special characters in path and snippet
            escaped_path = entry['path'].replace('|', '\\|')
            escaped_snippet = entry['snippet'].replace('|', '\\|').replace('\n', ' ').replace('\r', '')
            manifest_content += f"| `{escaped_path}` | {entry['size']} | `{escaped_snippet}` |\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(manifest_content)

    print(f"Manifest generated successfully at {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a markdown manifest of files in a directory."
    )
    parser.add_argument(
        "--directory", 
        required=True, 
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--output", 
        required=True, 
        help="The path to the output Markdown manifest file."
    )
    parser.add_argument(
        "--patterns", 
        nargs='*', 
        default=[], 
        help="One or more glob-style patterns (e.g., *.txt, report_*.log) to filter files. If not provided, all files are included."
    )
    parser.add_argument(
        "--snippet-length", 
        type=int, 
        default=0, 
        help="The number of characters to include as a content snippet for each file. Defaults to 0 (no snippet)."
    )

    args = parser.parse_args()

    try:
        generate_manifest(
            args.directory,
            args.patterns,
            args.output,
            args.snippet_length
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
