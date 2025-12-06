import os
import argparse
from pathlib import Path
from typing import List, Set

def scan_directory(
    root_path: Path,
    allowed_extensions: Set[str],
    filename_keywords: Set[str]
) -> List[Path]:
    """
    Scans a directory for files matching specified extensions or filename keywords.

    Args:
        root_path: The root directory to start scanning from.
        allowed_extensions: A set of lowercase file extensions to match (e.g., {".txt", ".md"}).
        filename_keywords: A set of lowercase keywords to match in filenames.

    Returns:
        A list of Path objects for files that match the criteria.
    """
    if not root_path.is_dir():
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    matching_files: List[Path] = []

    for dirpath, _, filenames in os.walk(root_path):
        current_dir = Path(dirpath)
        for filename in filenames:
            file_path = current_dir / filename
            file_name_lower = filename.lower()
            file_suffix_lower = file_path.suffix.lower()

            # Check if any criteria are provided. If not, all files match.
            if not allowed_extensions and not filename_keywords:
                matching_files.append(file_path)
                continue

            # Check for extension match
            extension_match = bool(allowed_extensions and file_suffix_lower in allowed_extensions)

            # Check for keyword match in filename
            keyword_match = bool(filename_keywords and any(kw in file_name_lower for kw in filename_keywords))

            if extension_match or keyword_match:
                matching_files.append(file_path)

    return matching_files

def main():
    parser = argparse.ArgumentParser(
        description="Scans directories for files matching specified extensions or filename keywords."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=[],
        help="A space-separated list of file extensions to look for (e.g., .txt .log). Case-insensitive."
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=[],
        help="A space-separated list of keywords to look for in filenames (e.g., report data). Case-insensitive."
    )

    args = parser.parse_args()

    root_path = Path(args.path)
    allowed_extensions = {ext.lower() for ext in args.extensions}
    filename_keywords = {kw.lower() for kw in args.keywords}

    if not allowed_extensions and not filename_keywords:
        print("Warning: No extensions or keywords provided. Listing all files.")

    found_files = scan_directory(root_path, allowed_extensions, filename_keywords)

    if found_files:
        print("\n--- Found Files ---")
        for f in sorted(found_files):
            print(f)
        print(f"\nTotal: {len(found_files)} files found.")
    else:
        print("\nNo files found matching the criteria.")

if __name__ == "__main__":
    main()
