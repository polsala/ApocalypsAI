import os
import re
import argparse
import json
from collections import defaultdict

# Define comment patterns for various types of annotations
# Each pattern captures the message after the tag.
COMMENT_PATTERNS = {
    "TODO": re.compile(r'#\s*TODO(?::|\s+)(.*)', re.IGNORECASE),
    "FIXME": re.compile(r'#\s*FIXME(?::|\s+)(.*)', re.IGNORECASE),
    "HACK": re.compile(r'#\s*HACK(?::|\s+)(.*)', re.IGNORECASE),
    "BUG": re.compile(r'#\s*BUG(?::|\s+)(.*)', re.IGNORECASE),
    "NOTE": re.compile(r'#\s*NOTE(?::|\s+)(.*)', re.IGNORECASE),
}

# File extensions to scan. Add more as needed.
# This is a simple heuristic; a more advanced version might use shebangs or file content analysis.
SCAN_FILE_EXTENSIONS = (
    '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rb', '.php', '.sh',
    '.md', '.txt', '.yml', '.yaml', '.json', '.xml', '.html', '.css', '.scss', '.less'
)

def scan_file(filepath: str, patterns: dict) -> list:
    """Scans a single file for defined comment patterns."""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for comment_type, pattern in patterns.items():
                    match = pattern.search(line)
                    if match:
                        message = match.group(1).strip() if match.group(1) else "No message provided."
                        findings.append({
                            "type": comment_type,
                            "line": line_num,
                            "message": message
                        })
    except IOError as e:
        print(f"Warning: Could not read file {filepath}: {e}")
    return findings

def scan_directory(
    directory: str,
    patterns: dict,
    exclude_dirs: list = None,
    exclude_files: list = None
) -> dict:
    """Recursively scans a directory for comment patterns in relevant files."""
    all_findings = defaultdict(list)
    exclude_dirs = [d.lower() for d in (exclude_dirs or [])]
    exclude_files = [f.lower() for f in (exclude_files or [])]

    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to exclude unwanted directories from traversal
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs]

        for filename in files:
            if filename.lower() in exclude_files:
                continue
            if not filename.lower().endswith(SCAN_FILE_EXTENSIONS):
                continue

            filepath = os.path.join(root, filename)
            file_findings = scan_file(filepath, patterns)
            if file_findings:
                all_findings[filepath].extend(file_findings)

    return dict(all_findings)

def generate_report(
    all_findings: dict,
    output_format: str = 'text'
) -> str:
    """Generates a formatted report from the findings."""
    total_findings = sum(len(f) for f in all_findings.values())
    summary_by_type = defaultdict(int)
    for filepath_findings in all_findings.values():
        for finding in filepath_findings:
            summary_by_type[finding['type']] += 1

    if output_format == 'json':
        report_data = {
            "total_findings": total_findings,
            "files": [
                {"filepath": fp, "findings": fs}
                for fp, fs in all_findings.items()
            ],
            "summary_by_type": dict(summary_by_type)
        }
        return json.dumps(report_data, indent=2)
    else: # text format
        report_lines = ["-- Code Comment Concierge Report ---", f"\nTotal Findings: {total_findings}"]

        for filepath, findings in all_findings.items():
            report_lines.append(f"\nFile: {filepath}")
            for finding in findings:
                report_lines.append(f"  L{finding['line']}: {finding['type']}: {finding['message']}")

        report_lines.append("\n--- Summary by Type ---")
        for comment_type, count in sorted(summary_by_type.items()):
            report_lines.append(f"{comment_type}: {count}")
        # Add types with 0 count for completeness
        for comment_type in COMMENT_PATTERNS.keys():
            if comment_type not in summary_by_type:
                report_lines.append(f"{comment_type}: 0")

        return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for TODOs, FIXMEs, HACKs, BUGs, and NOTE comments."
    )
    parser.add_argument(
        '--path', type=str, required=True,
        help='The root directory to start scanning from.'
    )
    parser.add_argument(
        '--exclude-dirs', nargs='*', default=[],
        help='Space-separated list of directory names to exclude (e.g., venv .git build).'
    )
    parser.add_argument(
        '--exclude-files', nargs='*', default=[],
        help='Space-separated list of file names to exclude (e.g., config.py temp.txt).'
    )
    parser.add_argument(
        '--output-format', type=str, choices=['text', 'json'], default='text',
        help='Specify the output format: text (default) or json.'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        exit(1)

    print(f"Scanning '{args.path}' for code comments...")
    findings = scan_directory(args.path, COMMENT_PATTERNS, args.exclude_dirs, args.exclude_files)
    report = generate_report(findings, args.output_format)
    print(report)

if __name__ == '__main__':
    main()
