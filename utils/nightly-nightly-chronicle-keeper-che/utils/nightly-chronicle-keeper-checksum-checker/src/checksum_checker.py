import os
import hashlib
import json
import argparse

def calculate_file_checksum(filepath, algorithm='sha256'):
    """Calculates the checksum of a file."""
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except FileNotFoundError:
        return None # Indicate file not found during checksum calculation
    return hasher.hexdigest()

def generate_manifest(directory, output_file, algorithm='sha256'):
    """
    Generates a checksum manifest for all files in a given directory.
    Paths in the manifest are relative to the directory.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return None

    manifest = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, directory)
            checksum = calculate_file_checksum(filepath, algorithm)
            if checksum is not None:
                manifest[relative_path] = checksum
            else:
                print(f"Warning: Could not calculate checksum for '{filepath}'. Skipping.")

    try:
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=4)
        print(f"Manifest generated at {output_file}")
        return manifest
    except IOError as e:
        print(f"Error writing manifest to '{output_file}': {e}")
        return None

def verify_manifest(directory, manifest_file, algorithm='sha256'):
    """
    Verifies files in a directory against a checksum manifest.
    Returns True if all files match and no extra files are found, False otherwise.
    """
    if not os.path.exists(manifest_file):
        print(f"Error: Manifest file not found at {manifest_file}")
        return False

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return False

    try:
        with open(manifest_file, 'r') as f:
            expected_manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing manifest file '{manifest_file}': {e}")
        return False
    except IOError as e:
        print(f"Error reading manifest file '{manifest_file}': {e}")
        return False

    current_manifest = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, directory)
            checksum = calculate_file_checksum(filepath, algorithm)
            if checksum is not None:
                current_manifest[relative_path] = checksum

    all_ok = True
    print(f"Verifying directory '{directory}' against manifest '{manifest_file}'...")

    # Check for missing or modified files
    for relative_path, expected_checksum in expected_manifest.items():
        if relative_path not in current_manifest:
            print(f"  MISSING: {relative_path}")
            all_ok = False
        elif current_manifest[relative_path] != expected_checksum:
            print(f"  MODIFIED: {relative_path} (Expected: {expected_checksum}, Found: {current_manifest[relative_path]}) - Checksum mismatch")
            all_ok = False
        # else:
        #     print(f"  OK: {relative_path}") # Too verbose for large directories

    # Check for unexpected new files
    for relative_path in current_manifest:
        if relative_path not in expected_manifest:
            print(f"  NEW: {relative_path} - Not in manifest")
            all_ok = False

    if all_ok:
        print("Verification successful: All files match the manifest.")
    else:
        print("Verification failed: Discrepancies found.")
    return all_ok

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper's Checksum Checker: Generate and verify file integrity manifests."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a checksum manifest for a directory.')
    generate_parser.add_argument('directory', help='The directory to scan.')
    generate_parser.add_argument('output_file', help='The output JSON file for the manifest.')
    generate_parser.add_argument('--algorithm', default='sha256', help='Checksum algorithm (e.g., sha256, md5). Default: sha256.')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify files in a directory against a manifest.')
    verify_parser.add_argument('directory', help='The directory to verify.')
    verify_parser.add_argument('manifest_file', help='The JSON manifest file to use for verification.')
    verify_parser.add_argument('--algorithm', default='sha256', help='Checksum algorithm (e.g., sha256, md5). Default: sha256.')

    args = parser.parse_args()

    if args.command == 'generate':
        generate_manifest(args.directory, args.output_file, args.algorithm)
    elif args.command == 'verify':
        verify_manifest(args.directory, args.manifest_file, args.algorithm)

if __name__ == '__main__':
    main()
