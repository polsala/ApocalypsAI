import os
import sys
from typing import List, Dict, Tuple

ESSENTIAL_FILES = {
    "README.md": "Project overview and instructions",
    "LICENSE": "Legal survival guide",
    "requirements.txt": "Python dependency rations",
    "Dockerfile": "Containerized shelter blueprint",
    "Makefile": "Build automation tools",
    ".gitignore": "Unwanted debris filter",
    "pyproject.toml": "Modern Python project manifest",
    "CONTRIBUTING.md": "Guidelines for contributing to the project",
}

ESSENTIAL_DIRS = {
    "docs": "Additional documentation directory",
}

def check_project_survival_kit(project_path: str) -> Tuple[List[str], List[str]]:
    """
    Scans the given project path for essential survival kit files and directories.

    Args:
        project_path: The path to the project directory.

    Returns:
        A tuple containing two lists: (missing_items, present_items).
    """
    if not os.path.isdir(project_path):
        print(f"Error: Project path '{project_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    missing_items: List[str] = []
    present_items: List[str] = []

    print(f"Scanning project at: {project_path}\n")
    print("--- Survival Kit Status ---\n")

    # Check for essential files
    for filename, description in ESSENTIAL_FILES.items():
        file_path = os.path.join(project_path, filename)
        if os.path.exists(file_path):
            print(f"✅ {filename} ({description})")
            present_items.append(filename)
        else:
            # Special check for Python dependency files: if pyproject.toml exists and has relevant sections
            if filename == "requirements.txt" and os.path.exists(os.path.join(project_path, "pyproject.toml")):
                try:
                    with open(os.path.join(project_path, "pyproject.toml"), 'r') as f:
                        content = f.read()
                        if "[tool.poetry]" in content or "[project]" in content:
                            print(f"✅ {filename} (Python dependency rations - via pyproject.toml)")
                            present_items.append(filename)
                            continue # Skip adding to missing if pyproject.toml covers it
                except IOError:
                    # If pyproject.toml exists but can't be read, treat as if it doesn't cover deps
                    pass
            print(f"❌ {filename} ({description})")
            missing_items.append(filename)

    # Check for essential directories
    for dirname, description in ESSENTIAL_DIRS.items():
        dir_path = os.path.join(project_path, dirname)
        if os.path.isdir(dir_path):
            print(f"✅ {dirname}/ ({description})")
            present_items.append(dirname + "/")
        else:
            print(f"❌ {dirname}/ ({description})")
            missing_items.append(dirname + "/")

    print("\n--- Summary ---")
    if missing_items:
        print(f"Your project is missing {len(missing_items)} essential survival items.")
        print("Consider adding: " + ", ".join(missing_items))
    else:
        print("Your project's survival kit is complete! Well done.")

    return missing_items, present_items

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/scavenger.py <path_to_project_directory>", file=sys.stderr)
        sys.exit(1)

    project_dir = sys.argv[1]
    missing, _ = check_project_survival_kit(project_dir)
    # Exit with 0 even if items are missing, as the utility successfully generated a report.
    # An exit code of 1 is reserved for actual runtime errors (e.g., invalid path).
    sys.exit(0)
