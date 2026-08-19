import os
import json
import sys

CONFIG_FILE = "config.json"
REQUIREMENTS_FILE = "/app/project/requirements.txt" # Expected mount point

def load_config(config_path):
    """Loads the configuration for heavy and unnecessary packages."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file at {config_path}", file=sys.stderr)
        sys.exit(1)

def parse_requirements(requirements_path):
    """Parses a requirements.txt file and returns a list of package names."""
    packages = []
    try:
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name before any version specifiers or comments
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('<')[0].split('>')[0].split('~=')[0].split(';')[0].strip()
                    if package_name:
                        packages.append(package_name.lower())
        return packages
    except FileNotFoundError:
        print(f"Warning: requirements.txt not found at {requirements_path}. Skipping dependency scan.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error parsing requirements.txt at {requirements_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    config = load_config(CONFIG_FILE)
    heavy_packages = {k.lower(): v for k, v in config.get("heavy_packages", {}).items()}
    unnecessary_packages = {p.lower() for p in config.get("unnecessary_packages", [])}

    print("--- Nightly Dependency Decontaminator Report ---")
    print(f"Scanning for dependencies in: {REQUIREMENTS_FILE}\n")

    project_packages = parse_requirements(REQUIREMENTS_FILE)

    if not project_packages:
        print("No dependencies found or requirements.txt is missing/empty. All clear!")
        return

    found_issues = False

    for package in project_packages:
        if package in heavy_packages:
            print(f"🚨 HEAVY DEPENDENCY DETECTED: '{package}'")
            print(f"   Suggestion: {heavy_packages[package]}\n")
            found_issues = True
        elif package in unnecessary_packages:
            print(f"⚠️ UNNECESSARY DEPENDENCY DETECTED: '{package}'")
            print(f"   Suggestion: This package might be bloat for a lean survival setup. Consider removal.\n")
            found_issues = True

    if not found_issues:
        print("✅ All dependencies appear lean and essential for survival. Good job!")
    else:
        print("--- Decontamination complete. Review detected issues. ---")

if __name__ == "__main__":
    main()
