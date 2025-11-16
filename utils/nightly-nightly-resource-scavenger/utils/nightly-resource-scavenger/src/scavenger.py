import os
import argparse
import sys

def is_text_file(filepath):
    """Heuristically checks if a file is likely a text file."""
    # This is a simple heuristic, not foolproof.
    # For robustness, one might check for common text encodings or use a library like 'chardet'.
    # For this utility, we'll keep it simple: if it can be opened and read as UTF-8 without error, it's text.
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024) # Read a chunk to check for decoding errors
        return True
    except UnicodeDecodeError:
        return False
    except Exception: # e.g., permission errors, directory
        return False

def scavenge_resources(directory, extensions, output_path, max_content_lines=5):
    """
    Scavenges a directory for files matching specified extensions and compiles a report.

    Args:
        directory (str): The root directory to start scavenging from.
        extensions (list): A list of file extensions (e.g., ['.txt', '.md']).
        output_path (str): The path to the output report file.
        max_content_lines (int): Maximum number of lines to include from each file's content.

    Returns:
        bool: True if the report was generated successfully, False otherwise.
    """
    report_lines = []
    found_files_count = 0

    report_lines.append(f"--- ApocalypsAI Resource Scavenger Report ---")
    report_lines.append(f"Scan initiated: {os.path.abspath(directory)}")
    report_lines.append(f"Target extensions: {', '.join(extensions)}")
    report_lines.append("-" * 50)

    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in extensions:
                    filepath = os.path.join(root, filename)
                    found_files_count += 1
                    report_lines.append(f"\n### Found Resource: {filepath}")
                    try:
                        file_size = os.path.getsize(filepath)
                        report_lines.append(f"Size: {file_size} bytes")

                        if is_text_file(filepath):
                            report_lines.append("Content Snippet:")
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                for i, line in enumerate(f):
                                    if i >= max_content_lines:
                                        report_lines.append(f"... (truncated after {max_content_lines} lines)")
                                        break
                                    report_lines.append(f"  {line.strip()}")
                        else:
                            report_lines.append("Content: [Binary or non-text file - content skipped]")

                    except Exception as e:
                        report_lines.append(f"Error processing file: {e}")
                    report_lines.append("-" * 30) # Separator for files

        report_lines.append(f"\n--- Scan Summary ---")
        report_lines.append(f"Total files found matching criteria: {found_files_count}")
        report_lines.append(f"Report generated at: {output_path}")
        report_lines.append(f"--- End of Report ---")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        return True

    except Exception as e:
        sys.stderr.write(f"Error during scavenging: {e}\n")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Resource Scavenger: Scans a directory for specified file types and generates a report."
    )
    parser.add_argument(
        "directory",
        help="The root directory to scavenge."
    )
    parser.add_argument(
        "-e", "--extensions",
        nargs='+',
        default=['.txt', '.md', '.log', '.json', '.yaml', '.yml'],
        help="List of file extensions to scavenge (e.g., .txt .md). Defaults to common text files."
    )
    parser.add_argument(
        "-o", "--output",
        default="scavenger_report.txt",
        help="Path to the output report file. Defaults to 'scavenger_report.txt'."
    )
    parser.add_argument(
        "-l", "--lines",
        type=int,
        default=5,
        help="Maximum number of content lines to include per file in the report. Defaults to 5."
    )

    args = parser.parse_args()

    # Ensure extensions start with a dot
    processed_extensions = [ext if ext.startswith('.') else f".{ext}" for ext in args.extensions]
    processed_extensions = [ext.lower() for ext in processed_extensions] # Ensure lowercase for comparison

    if not os.path.isdir(args.directory):
        sys.stderr.write(f"Error: Directory '{args.directory}' not found.\n")
        sys.exit(1)

    if scavenge_resources(args.directory, processed_extensions, args.output, args.lines):
        print(f"Scavenging complete. Report saved to '{args.output}'.")
        sys.exit(0)
    else:
        sys.stderr.write("Scavenging failed.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
