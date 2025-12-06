import os
import re
import argparse
from collections import defaultdict

def scan_logs(directory, patterns, file_extensions, max_snippets):
    """
    Scans log files in the given directory for specified patterns.

    Args:
        directory (str): The root directory to scan.
        patterns (list): A list of regex patterns or keywords to search for.
        file_extensions (list): A list of file extensions to consider as log files.
        max_snippets (int): Maximum number of snippets to show per pattern per file.

    Returns:
        dict: A dictionary containing scan results.
              Format: {file_path: {pattern: {'count': int, 'snippets': list}}}
    """
    results = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'snippets': []}))
    compiled_patterns = [(p, re.compile(p, re.IGNORECASE)) for p in patterns]

    for root, _, files in os.walk(directory):
        for file_name in files:
            if any(file_name.endswith(f".{ext}") for ext in file_extensions):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            for original_pattern, compiled_pattern in compiled_patterns:
                                if compiled_pattern.search(line):
                                    results[file_path][original_pattern]['count'] += 1
                                    if len(results[file_path][original_pattern]['snippets']) < max_snippets:
                                        results[file_path][original_pattern]['snippets'].append(
                                            f"[Line {line_num}] {line.strip()}"
                                        )
                except Exception as e:
                    # Log the error but continue scanning other files
                    print(f"Warning: Could not read file {file_path}: {e}")
    return results

def generate_report(results, directory, patterns, file_extensions, output_file=None):
    """
    Generates a human-readable report from the scan results.

    Args:
        results (dict): The scan results from scan_logs.
        directory (str): The scanned directory.
        patterns (list): The patterns used for scanning.
        file_extensions (list): The file extensions used.
        output_file (str, optional): Path to save the report. If None, prints to console.
    """
    report_lines = []
    report_lines.append("Luminator's Report - Scan Summary\n")
    report_lines.append(f"Scanning directory: {directory}")
    report_lines.append(f"Patterns searched: {', '.join(patterns)}")
    report_lines.append(f"File extensions: {', '.join(file_extensions)}\n")

    total_files_scanned = len(results)
    total_patterns_found = sum(sum(p_data['count'] for p_data in file_data.values()) for file_data in results.values())

    if not results:
        report_lines.append("No relevant log files found or no patterns matched.")
    else:
        for file_path, file_data in results.items():
            report_lines.append("---\n")
            report_lines.append(f"File: {file_path}")
            for pattern, data in file_data.items():
                report_lines.append(f"  Pattern '{pattern}': {data['count']} match{'es' if data['count'] != 1 else ''}")
                for i, snippet in enumerate(data['snippets']):
                    report_lines.append(f"    - [Snippet {i+1}] {snippet}")
            report_lines.append("") # Add an empty line for spacing

    report_lines.append("---\n")
    report_lines.append(f"Total files scanned: {total_files_scanned}")
    report_lines.append(f"Total pattern matches found: {total_patterns_found}")

    report_content = "\n".join(report_lines)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Report saved to {output_file}")
    else:
        print(report_content)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Luminator: Scans log files for critical patterns."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start scanning for log files."
    )
    parser.add_argument(
        "--patterns",
        required=True,
        help="A comma-separated list of keywords or regex patterns to search for."
    )
    parser.add_argument(
        "--extensions",
        default="log",
        help="A comma-separated list of file extensions to consider as log files (e.g., log,txt). Defaults to 'log'."
    )
    parser.add_argument(
        "--output",
        help="Path to save the report. If not provided, prints to console."
    )
    parser.add_argument(
        "--max-snippets",
        type=int,
        default=3,
        help="Maximum number of snippets to show per pattern per file. Defaults to 3."
    )

    args = parser.parse_args()

    directory = args.path
    patterns = [p.strip() for p in args.patterns.split(',')]
    file_extensions = [ext.strip() for ext in args.extensions.split(',')]
    max_snippets = args.max_snippets

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        exit(1)

    results = scan_logs(directory, patterns, file_extensions, max_snippets)
    generate_report(results, directory, patterns, file_extensions, args.output)

if __name__ == "__main__":
    main()
