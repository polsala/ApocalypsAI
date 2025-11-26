import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict

DEFAULT_ESSENTIAL_FILES = [
    "README.md",
    "LICENSE",
    ".gitignore",
    "requirements.txt",
    ".env",
]

def check_survival_kit(project_path: Path, essential_items: List[str]) -> Dict[str, bool]:
    """
    Checks a project directory for the presence of essential files or directories.

    Args:
        project_path: The root path of the project to check.
        essential_items: A list of file/directory names to consider essential.

    Returns:
        A dictionary where keys are essential item names and values are booleans
        indicating their presence (True) or absence (False).
    """
    results = {}
    for item in essential_items:
        item_path = project_path / item
        results[item] = item_path.exists()
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Survival Kit Checker: Ensures your project is apocalypse-ready!"
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory of the project to check."
    )
    parser.add_argument(
        "--files",
        type=str,
        default=",".join(DEFAULT_ESSENTIAL_FILES),
        help=f"A comma-separated list of essential files/directories to look for. Defaults to: {', '.join(DEFAULT_ESSENTIAL_FILES)}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show more detailed output, including present files."
    )

    args = parser.parse_args()

    project_path = Path(args.path)
    if not project_path.is_dir():
        print(f"\n🚨 ERROR: Project path '{args.path}' is not a valid directory. Aborting survival check!\n")
        sys.exit(1)

    essential_items = [f.strip() for f in args.files.split(',') if f.strip()]
    if not essential_items:
        print("\n⚠️ WARNING: No essential files/directories specified. Nothing to check!\n")
        sys.exit(0)

    print(f"\n--- Initiating Survival Kit Check for '{project_path.name}' ---")
    print(f"Scanning for: {', '.join(essential_items)}\n")

    results = check_survival_kit(project_path, essential_items)

    missing_count = 0
    present_count = 0

    for item, is_present in results.items():
        status = "✅ PRESENT" if is_present else "❌ MISSING"
        if not is_present:
            missing_count += 1
        else:
            present_count += 1
        if args.verbose or not is_present:
            print(f"  {status}: {item}")

    print("\n--- Survival Kit Summary ---")
    if missing_count == 0:
        print(f"🎉 All {present_count} essential items found! Your project is apocalypse-ready!")
    else:
        print(f"⚠️  {missing_count} essential items MISSING. {present_count} found. Prepare for potential fallout!")
        print("Consider reinforcing your project's defenses before the next digital storm.")
        sys.exit(1) # Indicate failure if essential items are missing

    print("----------------------------\n")


if __name__ == "__main__":
    main()
