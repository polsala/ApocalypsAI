import os
import re
import argparse
from typing import List, Dict, Tuple, Optional

# Regex to find keywords and capture the rest of the line
# It looks for a keyword followed by optional whitespace, then captures the rest of the line.
# It's case-insensitive for the keywords.
TANGLE_REGEX_TEMPLATE = r"(?i)\b({})\b\s*(.*)"

def find_tangles(
    directory: str,
    keywords: List[str],
    exclude_dirs: Optional[List[str]] = None
) -> Dict[str, List[Tuple[str, int, str]]]:
    """
    Scans a directory for specified keywords (tangles) in text files.

    Args:
        directory: The root directory to scan.
        keywords: A list of keywords to search for (e.g., ['TODO', 'FIXME']).
        exclude_dirs: Optional list of directory names to exclude from scanning.

    Returns:
        A dictionary where keys are file paths and values are lists of
        (keyword, line_number, comment_text) tuples.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")

    tangles_found: Dict[str, List[Tuple[str, int, str]]] = {}
    exclude_dirs_lower = [d.lower() for d in exclude_dirs] if exclude_dirs else []

    # Compile a single regex for all keywords for efficiency
    keyword_pattern = "|".join(re.escape(kw) for kw in keywords)
    full_regex = re.compile(TANGLE_REGEX_TEMPLATE.format(keyword_pattern))

    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to prune directories for os.walk
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs_lower]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not os.path.isfile(file_path):
                continue

            # Skip common binary/non-text files or files in common build/dependency directories
            if any(file_name.lower().endswith(ext) for ext in [
                '.pyc', '.o', '.so', '.dll', '.exe', '.bin', '.zip', '.tar.gz', '.gz', '.rar', '.7z',
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.mp3', '.wav', '.flac', '.mp4', '.avi', '.mov', '.mkv'
            ]) or \
               any(part.lower() in exclude_dirs_lower + ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 'build', 'dist'] for part in file_path.split(os.sep)):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        match = full_regex.search(line)
                        if match:
                            keyword = match.group(1).upper() # Ensure keyword is uppercase for consistency
                            comment_text = match.group(2).strip()
                            if file_path not in tangles_found:
                                tangles_found[file_path] = []
                            tangles_found[file_path].append((keyword, line_num, comment_text))
            except Exception:
                # Silently skip files that cause read errors (e.g., truly binary files or permission issues)
                pass
    return tangles_found

def generate_report(
    tangles: Dict[str, List[Tuple[str, int, str]]],
    base_path: str = ""
) -> str:
    """
    Generates a Markdown report from the found tangles.

    Args:
        tangles: The dictionary of found tangles.
        base_path: An optional base path to make file paths relative to in the report.

    Returns:
        A Markdown formatted string report.
    """
    if not tangles:
        return "## No Temporal Tangles Found! ✨\n\nYour codebase is sparkling clean (from known tangles, at least).\n"

    report_lines: List[str] = ["# Temporal Tangle Report 🕸️\n", "## Unearthing Forgotten Intentions\n"]

    # Sort files for consistent report generation
    sorted_files = sorted(tangles.keys())

    for file_path in sorted_files:
        relative_path = os.path.relpath(file_path, base_path) if base_path else file_path
        report_lines.append(f"### File: `{relative_path}`\n")
        
        # Group tangles by keyword within each file
        tangles_by_keyword: Dict[str, List[Tuple[int, str]]] = {}
        for keyword, line_num, comment_text in tangles[file_path]:
            if keyword not in tangles_by_keyword:
                tangles_by_keyword[keyword] = []
            tangles_by_keyword[keyword].append((line_num, comment_text))
        
        # Sort keywords and then tangles within each keyword group
        for keyword in sorted(tangles_by_keyword.keys()):
            report_lines.append(f"#### `{keyword}`\n")
            for line_num, comment_text in sorted(tangles_by_keyword[keyword], key=lambda x: x[0]):
                report_lines.append(f"- Line {line_num}: {comment_text}\n")
        report_lines.append("\n") # Add a newline for spacing between files

    report_lines.append("---\n")
    report_lines.append("Generated by ApocalypsAI's Nightly Temporal Tangle Tracker 🤖")
    return "".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for TODO/FIXME/HACK comments and generate a report."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--keywords",
        nargs='*',
        default=['TODO', 'FIXME', 'HACK'],
        help="Space-separated list of keywords to search for. Defaults to 'TODO', 'FIXME', 'HACK'."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the Markdown report. If not provided, prints to stdout."
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs='*',
        default=['.git', '__pycache__', 'node_modules', '.venv', 'venv', 'build', 'dist'],
        help="Space-separated list of directory names to exclude from scanning (case-insensitive)."
    )

    args = parser.parse_args()

    try:
        tangles = find_tangles(args.path, args.keywords, args.exclude_dirs)
        report = generate_report(tangles, base_path=args.path)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
