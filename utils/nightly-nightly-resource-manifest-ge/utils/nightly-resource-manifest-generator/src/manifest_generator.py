import argparse
import os
import json
import re
from datetime import datetime
import toml # For Cargo.toml

def parse_requirements_txt(file_path):
    """Parses a requirements.txt file."""
    dependencies = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                dependencies.append(line)
    return dependencies

def parse_package_json(file_path):
    """Parses package.json for dependencies and devDependencies."""
    dependencies = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        for dep_type in ['dependencies', 'devDependencies']:
            if dep_type in data:
                for pkg, version in data[dep_type].items():
                    dependencies.append(f"{pkg}: {version}")
    return dependencies

def parse_go_mod(file_path):
    """Parses a go.mod file for required modules."""
    dependencies = []
    with open(file_path, 'r') as f:
        in_require_block = False
        for line in f:
            line = line.strip()
            if line.startswith('require ('):
                in_require_block = True
                continue
            elif line == ')':
                in_require_block = False
                continue

            if in_require_block or line.startswith('require '):
                parts = line.split()
                if len(parts) >= 3 and parts[0] == 'require': # Single line require
                    pkg = parts[1]
                    version = parts[2]
                    dependencies.append(f"{pkg} {version}")
                elif len(parts) >= 2 and in_require_block: # Inside a require block
                    pkg = parts[0]
                    version = parts[1]
                    dependencies.append(f"{pkg} {version}")
    return dependencies

def parse_cargo_toml(file_path):
    """Parses Cargo.toml for [dependencies]."""
    dependencies = []
    try:
        with open(file_path, 'r') as f:
            data = toml.load(f)
            if 'dependencies' in data:
                for pkg, version_info in data['dependencies'].items():
                    if isinstance(version_info, dict):
                        # Handle complex versions like { version = "1.2.3", features = ["full"] }
                        # Sort keys for deterministic output
                        sorted_items = sorted(version_info.items())
                        version_str = f"{{ {', '.join([f'{k} = \"{v}\"' if isinstance(v, str) else f'{k} = {v}' for k, v in sorted_items])} }}"
                        dependencies.append(f"{pkg} = {version_str}")
                    else:
                        dependencies.append(f"{pkg} = \"{version_info}\"")
    except Exception as e:
        print(f"Warning: Could not parse Cargo.toml at {file_path}: {e}")
    return dependencies


def generate_manifest(root_path, output_file):
    """
    Scans the root_path for dependency files and generates a Markdown manifest.
    """
    all_dependencies = {
        "Python": [],
        "Node.js": [],
        "Go": [],
        "Rust": []
    }

    dependency_parsers = {
        "requirements.txt": ("Python", parse_requirements_txt),
        "package.json": ("Node.js", parse_package_json),
        "go.mod": ("Go", parse_go_mod),
        "Cargo.toml": ("Rust", parse_cargo_toml),
    }

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename in dependency_parsers:
                file_path = os.path.join(dirpath, filename)
                lang, parser_func = dependency_parsers[filename]
                try:
                    deps = parser_func(file_path)
                    all_dependencies[lang].extend(deps)
                except Exception as e:
                    print(f"Warning: Failed to parse {file_path}: {e}")

    # Format into Markdown
    manifest_content = [
        "# Project Resource Manifest",
        f"\nGenerated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    ]

    for lang, deps in all_dependencies.items():
        if deps:
            manifest_content.append(f"## {lang} Dependencies\n")
            for dep in sorted(list(set(deps))): # Use set to remove duplicates, then sort
                manifest_content.append(f"*   {dep}")
            manifest_content.append("") # Add a blank line for spacing

    final_manifest = "\n".join(manifest_content).strip() + "\n" # Ensure trailing newline

    with open(output_file, 'w') as f:
        f.write(final_manifest)

    print(f"Manifest generated successfully at: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a consolidated resource manifest from project dependency files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for dependency files."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="The path where the generated Markdown manifest will be saved."
    )
    args = parser.parse_args()

    # Ensure toml is available for Cargo.toml parsing
    try:
        import toml
    except ImportError:
        print("Error: 'toml' library not found. Please install it: pip install toml")
        exit(1)

    generate_manifest(args.path, args.output)
