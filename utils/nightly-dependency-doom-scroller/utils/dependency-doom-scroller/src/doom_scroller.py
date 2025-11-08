import os
import re
import requests
import json
import argparse

# Mock rationale: In a real scenario, this would query PyPI's JSON API.
# For deterministic and offline testing, we mock `requests.get` to return
# predefined responses, simulating PyPI's behavior without actual network calls.
PYPI_API_URL = "https://pypi.org/pypi/{package_name}/json"

def _get_latest_version(package_name):
    """Fetches the latest version of a package from PyPI."""
    try:
        response = requests.get(PYPI_API_URL.format(package_name=package_name), timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        return data['info']['version']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest version for {package_name}: {e}")
        return None
    except KeyError:
        print(f"Could not find version info for {package_name} on PyPI or JSON structure is unexpected.")
        return None

def _parse_requirements(file_path):
    """Parses a requirements.txt file and returns a list of (package_name, version) tuples."""
    packages = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue # Skip empty lines and comments
                
                # Regex to match package name and optional version (e.g., 'package==1.0.0', 'package>=1.0.0', 'package')
                # Captures the package name and the version string if any operator is present.
                match = re.match(r'^([a-zA-Z0-9._-]+)(?:[<=>!~]=([0-9.]+))?.*', line)
                if match:
                    package_name = match.group(1)
                    version = match.group(2) # Will be None if no version specified or only operator without version
                    packages.append((package_name, version))
        return packages
    except FileNotFoundError:
        print(f"Error: requirements file not found at {file_path}")
        return []

def main(directory='.'):
    """Main function to scan for outdated dependencies."""
    req_file_path = os.path.join(directory, 'requirements.txt')

    if not os.path.exists(req_file_path):
        print(f"No 'requirements.txt' found in '{directory}'. The cosmic archives are silent.")
        return

    print("Scanning for signs of dependency decay...\n")
    print("--- The Scrolls of Prophecy Reveal ---\n")

    packages_to_check = _parse_requirements(req_file_path)
    if not packages_to_check:
        print("The scrolls are blank. No dependencies found to scrutinize.")
        return

    for package_name, current_version in packages_to_check:
        if current_version is None:
            print(f"⚠️ CAUTION: '{package_name}' has no version specified. The future is uncertain! (Consider pinning a version)")
            continue

        latest_version = _get_latest_version(package_name)

        if latest_version is None:
            print(f"❓ UNKNOWN: Could not determine the fate of '{package_name}'. Its cosmic signature is elusive.")
        else:
            # Attempt to use packaging.version.parse for robust version comparison
            # Fallback to simple string comparison if 'packaging' is not installed.
            try:
                from packaging.version import parse as parse_version
                if parse_version(latest_version) > parse_version(current_version):
                     print(f"🚨 WARNING: The ancient scroll for '{package_name}' (v{current_version}) is crumbling! A newer, more powerful version (v{latest_version}) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!")
                else:
                    print(f"✅ All clear for '{package_name}'. Its cosmic alignment is stable (v{current_version}).")
            except ImportError:
                # Fallback to simple string comparison if packaging is not available
                # This might not be accurate for all version schemes (e.g., '1.10' vs '1.9')
                if latest_version > current_version:
                    print(f"🚨 WARNING: The ancient scroll for '{package_name}' (v{current_version}) is crumbling! A newer, more powerful version (v{latest_version}) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!")
                else:
                    print(f"✅ All clear for '{package_name}'. Its cosmic alignment is stable (v{current_version}).")

    print("\n--- End of Prophecy ---\n")
    print("May your dependencies ever be current, and your project endure the ages.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scan project dependencies for outdated packages.")
    parser.add_argument('--directory', type=str, default='.',
                        help="The directory to scan for 'requirements.txt'. Defaults to current directory.")
    args = parser.parse_args()
    main(directory=args.directory)
