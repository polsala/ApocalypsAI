import os
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

def check_trailing_whitespace(filepath: Path) -> List[Tuple[int, str]]:
    """Checks a file for lines with trailing whitespace."""
    quirks = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if line.rstrip('\n') != line.rstrip(): # Check if rstrip removes more than just newline
                    quirks.append((i, line.rstrip('\n')))
    except UnicodeDecodeError:
        # Skip binary files or files with non-utf8 encoding
        pass
    except Exception as e:
        print(f"Warning: Could not read {filepath} for whitespace check: {e}")
    return quirks

def check_file_casing(filepath: Path, canonical_names: Dict[str, str]) -> List[str]:
    """Checks if a file's casing matches a canonical form."""
    quirks = []
    filename = filepath.name
    if filename.lower() in canonical_names:
        expected_name = canonical_names[filename.lower()]
        if filename != expected_name:
            quirks.append(f"Expected '{expected_name}', found '{filename}'")
    return quirks

def check_empty_file(filepath: Path) -> bool:
    """Checks if a file is empty."""
    try:
        return filepath.is_file() and filepath.stat().st_size == 0
    except Exception:
        return False # If we can't stat it, assume not empty or not a file

def scan_directory(root_dir: Path, canonical_files: List[str], text_file_extensions: List[str]) -> Dict[str, List[str]]:
    """Scans a directory for various quirks."""
    all_quirks: Dict[str, List[str]] = {
        "trailing_whitespace": [],
        "inconsistent_casing": [],
        "empty_files": []
    }

    canonical_map = {name.lower(): name for name in canonical_files}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = Path(dirpath) / filename

            # Check for inconsistent casing
            casing_quirks = check_file_casing(filepath, canonical_map)
            if casing_quirks:
                all_quirks["inconsistent_casing"].extend([f"{filepath}: {q}" for q in casing_quirks])

            # Check for empty files
            if check_empty_file(filepath):
                all_quirks["empty_files"].append(str(filepath))

            # Check for trailing whitespace (only for known text file types or canonical files)
            if filepath.suffix.lower() in text_file_extensions or filepath.name.lower() in canonical_map:
                whitespace_quirks = check_trailing_whitespace(filepath)
                for line_num, line_content in whitespace_quirks:
                    all_quirks["trailing_whitespace"].append(f"{filepath}:{line_num}: Trailing whitespace: '{line_content}'")

    return all_quirks

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for common file and content quirks."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for quirks."
    )
    args = parser.parse_args()

    root_dir = Path(args.directory)
    if not root_dir.is_dir():
        print(f"Error: Directory '{root_dir}' not found.")
        exit(1)

    canonical_files = ["README.md", "LICENSE", "AGENTS.md", ".gitignore"]
    text_file_extensions = [
        ".py", ".md", ".txt", ".yml", ".yaml", ".json", ".sh", ".css", ".html",
        ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".xml", ".toml"
    ]

    print(f"Scanning '{root_dir}' for quirks...")
    quirks = scan_directory(root_dir, canonical_files, text_file_extensions)

    found_any_quirks = False
    for quirk_type, quirk_list in quirks.items():
        if quirk_list:
            found_any_quirks = True
            print(f"\n--- {quirk_type.replace('_', ' ').title()} ---")
            for quirk in quirk_list:
                print(f"  - {quirk}")

    if not found_any_quirks:
        print("\nNo quantum quirks detected! Your repository is pristine.")
        exit(0)
    else:
        print("\nQuantum quirks detected! Time to quibble.")
        exit(1) # Exit with 1 if quirks are found, indicating a need for action

if __name__ == "__main__":
    main()
