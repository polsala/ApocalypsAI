import os
import re
import argparse
from typing import List, Dict, Any

# Regex to find common stale comment markers in Python files
# It looks for '# (TODO|FIXME|HACK|NOTE)[: ]' followed by any text.
STALE_COMMENT_PATTERN = re.compile(r"#\s*(TODO|FIXME|HACK|NOTE)[:\s].*", re.IGNORECASE)

def find_stale_comments_in_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Scans a single Python file for stale comments.
    Returns a list of dictionaries, each containing 'file', 'line', and 'content'.
    """
    found_comments = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if STALE_COMMENT_PATTERN.search(line):
                    found_comments.append({
                        'file': filepath,
                        'line': line_num,
                        'content': line.strip()
                    })
    except Exception as e:
        print(f"Warning: Could not read file {filepath}: {e}")
    return found_comments

def scan_directory(
    root_path: str,
    exclude_dirs: List[str] = None,
    exclude_files: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Scans a directory recursively for Python files containing stale comments.
    """
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []

    all_stale_comments = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Modify dirnames in-place to prune directories for os.walk
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            if filename.endswith('.py') and filename not in exclude_files:
                filepath = os.path.join(dirpath, filename)
                all_stale_comments.extend(find_stale_comments_in_file(filepath))
    return all_stale_comments

def main():
    parser = argparse.ArgumentParser(
        description="Scan Python files for stale comments (TODO, FIXME, HACK, NOTE)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs='*',
        default=[],
        help="Space-separated list of directory names to exclude (e.g., venv .git)."
    )
    parser.add_argument(
        "--exclude-files",
        nargs='*',
        default=[],
        help="Space-separated list of file names to exclude (e.g., setup.py __init__.py)."
    )

    args = parser.parse_args()

    print(f"Scanning {args.path}...")

    stale_comments = scan_directory(args.path, args.exclude_dirs, args.exclude_files)

    if stale_comments:
        print(f"\nFound {len(stale_comments)} stale comments:")
        print("-" * 50)
        for comment in stale_comments:
            print(f"File: {comment['file']}, Line: {comment['line']}")
            print(f"  {comment['content']}")
            print("-" * 50)
    else:
        print("\nNo stale comments found. Your codebase is sparkling clean! ✨")

    print("\nComposting complete! Time to clean up.")

if __name__ == "__main__":
    main()
