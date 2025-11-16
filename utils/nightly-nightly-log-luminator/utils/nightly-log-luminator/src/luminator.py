import argparse
import os
import re
from collections import defaultdict
from datetime import datetime

DEFAULT_PATTERNS = [
    r"ERROR",
    r"FAIL",
    r"Exception:",
    r"Traceback \(most recent call last\):",
    r"CRITICAL",
    r"WARN",
    r"WARNING",
    r"denied",
    r"timeout",
]

def scan_log_file(filepath: str, patterns: list[str]) -> dict:
    """Scans a single log file for specified patterns."""
    results = defaultdict(lambda: {'count': 0, 'unique_messages': defaultdict(int)})
    compiled_patterns = [(p, re.compile(p, re.IGNORECASE)) for p in patterns]

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern_str, compiled_pattern in compiled_patterns:
                    match = compiled_pattern.search(line)
                    if match:
                        results[pattern_str]['count'] += 1
                        # Store a snippet or the full line as a unique message
                        message = line.strip()
                        results[pattern_str]['unique_messages'][message] += 1
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return results

def generate_summary_report(all_results: dict, output_file: str | None = None) -> str:
    """Generates a markdown summary report from scan results."""
    report_lines = []
    report_lines.append(f"# 🔦 Nightly Log Luminator Report 🔦")
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if not all_results:
        report_lines.append("No relevant patterns found across scanned logs. All clear!")
        return "\n".join(report_lines)

    total_issues = 0
    for filepath, file_results in all_results.items():
        for pattern_str, data in file_results.items():
            total_issues += data['count']

    report_lines.append(f"## 📊 Overall Summary")
    report_lines.append(f"Total patterns detected: **{total_issues}**\n")

    for filepath, file_results in all_results.items():
        report_lines.append(f"## 📄 File: `{filepath}`")
        file_total_patterns = sum(data['count'] for data in file_results.values())
        report_lines.append(f"Total patterns in this file: **{file_total_patterns}**\n")

        if not file_results:
            report_lines.append("No patterns found in this file.\n")
            continue

        for pattern_str, data in file_results.items():
            report_lines.append(f"### Pattern: `{pattern_str}` (Count: {data['count']})")
            report_lines.append("#### Unique Messages:")
            sorted_messages = sorted(data['unique_messages'].items(), key=lambda item: item[1], reverse=True)
            for msg, count in sorted_messages[:5]: # Show top 5 unique messages
                report_lines.append(f"- `{msg}` (x{count})")
            if len(sorted_messages) > 5:
                report_lines.append(f"- ... and {len(sorted_messages) - 5} more unique messages.")
            report_lines.append("") # Add a blank line for spacing

    report_content = "\n".join(report_lines)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Report saved to {output_file}")
        except Exception as e:
            print(f"Error writing report to {output_file}: {e}")
    else:
        print(report_content)
    
    return report_content

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Luminator: Scans log files for patterns and generates a summary report."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to a log file or a directory containing log files."
    )
    parser.add_argument(
        "--output-file",
        help="Optional. Path to save the summary report. If not provided, prints to stdout."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=DEFAULT_PATTERNS,
        help="Optional. List of regex patterns to search for. Defaults to common error patterns."
    )

    args = parser.parse_args()

    all_results = defaultdict(dict)
    
    if os.path.isfile(args.path):
        print(f"Scanning file: {args.path}")
        file_results = scan_log_file(args.path, args.patterns)
        if file_results:
            all_results[args.path] = file_results
    elif os.path.isdir(args.path):
        print(f"Scanning directory: {args.path}")
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(('.log', '.txt')): # Only process common log/text files
                    filepath = os.path.join(root, file)
                    print(f"  Scanning {filepath}")
                    file_results = scan_log_file(filepath, args.patterns)
                    if file_results:
                        all_results[filepath] = file_results
    else:
        print(f"Error: Path '{args.path}' is neither a file nor a directory.")
        exit(1)

    generate_summary_report(all_results, args.output_file)

if __name__ == "__main__":
    main()
