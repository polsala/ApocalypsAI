import os
import argparse
from typing import List, Dict, Tuple

CRITTER_KEYWORDS = ["TODO", "FIXME", "BUG", "HACK"]
DEFAULT_EXTENSIONS = [
    ".py", ".js", ".ts", ".go", ".java", ".c", ".cpp", ".h", ".hpp", ".sh", ".md",
    ".rb", ".php", ".swift", ".kt", ".rs", ".vue", ".jsx", ".tsx", ".html", ".css", ".scss", ".less"
]
DEFAULT_EXCLUDE_DIRS = [
    ".git", "__pycache__", "node_modules", "venv", ".vscode", ".idea", "dist", "build",
    "target", "out", "bin", "tmp", "temp", ".DS_Store"
]

def find_critters_in_file(filepath: str) -> List[Tuple[int, str]]:
    """
    Scans a single file for critter keywords.
    Returns a list of (line_number, line_content) for each critter found.
    """
    critters_found = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for keyword in CRITTER_KEYWORDS:
                    if keyword in line.upper(): # Case-insensitive check
                        critters_found.append((i, line.strip()))
                        break # Only report one critter per line to avoid duplicates if multiple keywords are on the same line
    except Exception as e:
        # print(f"Warning: Could not read file {filepath}: {e}") # For debugging, but keep silent for production
        pass # Silently skip unreadable files
    return critters_found

def scan_directory_for_critters(
    root_dir: str,
    include_extensions: List[str],
    exclude_dirs: List[str]
) -> Dict[str, List[Tuple[int, str]]]:
    """
    Walks through a directory, finds files matching extensions, and scans them for critters.
    Returns a dictionary where keys are file paths and values are lists of (line_number, line_content).
    """
    all_critters: Dict[str, List[Tuple[int, str]]] = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to prune directories for os.walk
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext.lower() in include_extensions:
                filepath = os.path.join(dirpath, filename)
                critters = find_critters_in_file(filepath)
                if critters:
                    all_critters[filepath] = critters
    return all_critters

def generate_report(critter_data: Dict[str, List[Tuple[int, str]]], root_dir: str) -> str:
    """
    Generates a formatted report string from the critter data.
    """
    report_lines = [f"Critter Report for: {root_dir}\n"]
    total_critters = 0
    total_files = len(critter_data)

    if not critter_data:
        report_lines.append("No critters found. Your codebase is sparkling clean!")
        return "\n".join(report_lines)

    for filepath, critters in critter_data.items():
        report_lines.append("---\nFile: " + filepath)
        for line_num, line_content in critters:
            report_lines.append(f"  Line {line_num}: {line_content}")
        total_critters += len(critters)

    report_lines.append(f"---\nTotal Critters Found: {total_critters} in {total_files} files.")
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Scan code files for common 'critter' comments (TODO, FIXME, BUG, HACK) and generate a consolidated report."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default=",".join([ext.lstrip('.') for ext in DEFAULT_EXTENSIONS]),
        help=f"Comma-separated list of file extensions to include (e.g., py,js,md). Defaults to: {','.join([ext.lstrip('.') for ext in DEFAULT_EXTENSIONS])}"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default=",".join(DEFAULT_EXCLUDE_DIRS),
        help=f"Comma-separated list of directory names to exclude (e.g., venv,node_modules). Defaults to: {','.join(DEFAULT_EXCLUDE_DIRS)}"
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    if not os.path.isdir(root_path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.")
        exit(1)

    include_extensions = [f".{ext.strip().lower()}" for ext in args.extensions.split(',')]
    exclude_dirs = [d.strip() for d in args.exclude.split(',')]

    critter_data = scan_directory_for_critters(root_path, include_extensions, exclude_dirs)
    report = generate_report(critter_data, root_path)
    print(report)

if __name__ == "__main__":
    main()
