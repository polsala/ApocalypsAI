import argparse
import os
import re
import requests
import sys

PYPI_URL_TEMPLATE = "https://pypi.org/pypi/{package_name}/json"

def parse_simple_version(version_string):
    """Parses a version string into a tuple of integers for simple comparison."""
    try:
        # Extract the numeric parts of the version (e.g., '1.2.3' from '1.2.3rc1')
        base_version_match = re.match(r'^(\d+(\.\d+)*)', version_string)
        if base_version_match:
            return tuple(map(int, base_version_match.group(1).split('.')))
        return (0,) # Fallback for unparseable or empty versions
    except ValueError:
        return (0,) # Fallback for non-integer parts

def parse_requirements(req_file_path):
    """Parses a requirements.txt file and extracts package names and pinned versions."""
    dependencies = []
    if not os.path.exists(req_file_path):
        return dependencies

    with open(req_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Regex to capture package name and optional version specifier
            # e.g., 'requests==2.28.1', 'rich', 'flask>=2.0.0'
            match = re.match(r'^([a-zA-Z0-9._-]+)(==|>=|<=|>|<|~=)?(.*)$', line)
            if match:
                pkg_name = match.group(1)
                operator = match.group(2)
                version_spec = match.group(3).strip()

                if operator == '==':
                    dependencies.append({'name': pkg_name, 'pinned_version': version_spec})
                else:
                    # For any other operator or no operator, we consider it not strictly pinned
                    dependencies.append({'name': pkg_name, 'pinned_version': None})
            else:
                # Fallback for lines that are just package names without any specifier
                dependencies.append({'name': line, 'pinned_version': None})

    return dependencies

def get_latest_pypi_version(package_name):
    """Fetches the latest version of a package from PyPI."""
    try:
        response = requests.get(PYPI_URL_TEMPLATE.format(package_name=package_name), timeout=5)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data['info']['version']
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not fetch info for {package_name} from PyPI: {e}", file=sys.stderr)
        return None
    except KeyError:
        print(f"Warning: Could not find version info for {package_name} on PyPI (KeyError).", file=sys.stderr)
        return None

def stabilize_dependencies(project_path):
    """Scans project dependencies and reports on available updates."""
    req_file_path = os.path.join(project_path, 'requirements.txt')
    if not os.path.exists(req_file_path):
        print(f"No requirements.txt found in {project_path}. Nothing to stabilize.", file=sys.stderr)
        return []

    print(f"Scanning {req_file_path} for quantum fluctuations...")
    dependencies = parse_requirements(req_file_path)
    stabilization_report = []

    for dep in dependencies:
        pkg_name = dep['name']
        pinned_version = dep['pinned_version']
        latest_version = get_latest_pypi_version(pkg_name)

        if latest_version:
            if pinned_version:
                if parse_simple_version(latest_version) > parse_simple_version(pinned_version):
                    stabilization_report.append({
                        'package': pkg_name,
                        'current_version': pinned_version,
                        'latest_version': latest_version,
                        'status': 'UPDATE_AVAILABLE'
                    })
                else:
                    stabilization_report.append({
                        'package': pkg_name,
                        'current_version': pinned_version,
                        'latest_version': latest_version,
                        'status': 'UP_TO_DATE'
                    })
            else:
                # Not pinned, just report the latest available version
                stabilization_report.append({
                    'package': pkg_name,
                    'current_version': 'N/A (not pinned)',
                    'latest_version': latest_version,
                    'status': 'LATEST_REPORTED'
                })
        else:
            stabilization_report.append({
                'package': pkg_name,
                'current_version': pinned_version if pinned_version else 'N/A',
                'latest_version': 'N/A',
                'status': 'UNAVAILABLE'
            })

    return stabilization_report

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Dependency Stabilizer: Shoring up the temporal integrity of your project's dependencies."
    )
    parser.add_argument(
        '--project-path',
        type=str,
        default='.',
        help='Path to the project directory containing requirements.txt. Defaults to current directory.'
    )
    args = parser.parse_args()

    report = stabilize_dependencies(args.project_path)

    if not report:
        print("No dependencies found or no requirements.txt. The quantum fabric is stable (or non-existent).")
        sys.exit(2) # No-op: nothing to change/report

    print("\n--- Quantum Fluctuation Report ---")
    updates_found = False
    for item in report:
        if item['status'] == 'UPDATE_AVAILABLE':
            print(f"🚨 {item['package']}: Pinned to {item['current_version']}, but {item['latest_version']} is available! Consider `pip install {item['package']}=={item['latest_version']}`")
            updates_found = True
        elif item['status'] == 'LATEST_REPORTED':
            print(f"✨ {item['package']}: Not pinned, latest available is {item['latest_version']}.")
        elif item['status'] == 'UP_TO_DATE':
            print(f"✅ {item['package']}: Pinned to {item['current_version']}, which is the latest available ({item['latest_version']}).")
        elif item['status'] == 'UNAVAILABLE':
            print(f"❓ {item['package']}: Could not determine status. PyPI information unavailable.")

    if updates_found:
        print("\nTemporal integrity compromised! Consider applying the suggested updates to stabilize the project.")
    else:
        print("\nAll dependencies appear stable. The quantum fabric holds!")

    sys.exit(0) # Success: report generated, even if updates are found

if __name__ == '__main__':
    main()
