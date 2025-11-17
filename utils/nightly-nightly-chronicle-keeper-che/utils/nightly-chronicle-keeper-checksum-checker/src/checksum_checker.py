import hashlib
import json
import os
import argparse
from pathlib import Path

def calculate_sha256(filepath: Path) -> str:
    """Calculates the SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string in chunks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(directory: Path, output_file: Path):
    """
    Generates a JSON manifest of SHA256 checksums for all files in a directory.
    Paths in the manifest are relative to the given directory.
    """
    if not directory.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return 1

    manifest = {}
    print(f"Scanning '{directory}' for files...")
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = Path(root) / filename
            relative_path = filepath.relative_to(directory)
            try:
                checksum = calculate_sha256(filepath)
                manifest[str(relative_path)] = checksum
                print(f"  - {relative_path}: {checksum}")
            except Exception as e:
                print(f"  - Error processing {relative_path}: {e}")
                # Continue processing other files even if one fails

    try:
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=4)
        print(f"\nManifest generated successfully: '{output_file}' with {len(manifest)} entries.")
        return 0
    except Exception as e:
        print(f"Error writing manifest to '{output_file}': {e}")
        return 1

def verify_manifest(directory: Path, manifest_file: Path):
    """
    Verifies files in a directory against a previously generated manifest.
    Reports missing files, changed files, and new files.
    """
    if not directory.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return 1
    if not manifest_file.is_file():
        print(f"Error: Manifest file '{manifest_file}' does not exist.")
        return 1

    try:
        with open(manifest_file, 'r') as f:
            expected_manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in manifest file '{manifest_file}': {e}")
        return 1
    except Exception as e:
        print(f"Error reading manifest file '{manifest_file}': {e}")
        return 1

    current_files = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = Path(root) / filename
            relative_path = filepath.relative_to(directory)
            current_files[str(relative_path)] = filepath

    discrepancies = []
    matched_count = 0

    # Check for changed or missing files
    for relative_path_str, expected_checksum in expected_manifest.items():
        if relative_path_str not in current_files:
            discrepancies.append(f"- MISSING: {relative_path_str}")
        else:
            current_filepath = current_files[relative_path_str]
            try:
                actual_checksum = calculate_sha256(current_filepath)
                if actual_checksum != expected_checksum:
                    discrepancies.append(
                        f"- CHANGED: {relative_path_str} (Expected: {expected_checksum}, Found: {actual_checksum})"
                    )
                else:
                    matched_count += 1
            except Exception as e:
                discrepancies.append(f"- ERROR_READING: {relative_path_str} ({e})")

    # Check for new files not in manifest
    for relative_path_str in current_files:
        if relative_path_str not in expected_manifest:
            discrepancies.append(f"- NEW: {relative_path_str}")

    if discrepancies:
        print("\nVerification found discrepancies:")
        for d in discrepancies:
            print(d)
        print("Verification FAILED.")
        return 1
    else:
        print(f"\nVerification successful. All {matched_count} files match the manifest.")
        return 0

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper Checksum Checker: Generate and verify SHA256 checksums for files."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a new checksum manifest.')
    generate_parser.add_argument('--path', type=str, required=True,
                                 help='The directory to scan for files.')
    generate_parser.add_argument('--output', type=str, required=True,
                                 help='The output JSON file for the manifest.')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify files against an existing manifest.')
    verify_parser.add_argument('--path', type=str, required=True,
                                help='The directory to verify.')
    verify_parser.add_argument('--manifest', type=str, required=True,
                                help='The path to the manifest JSON file.')

    args = parser.parse_args()

    if args.command == 'generate':
        exit_code = generate_manifest(Path(args.path), Path(args.output))
        exit(exit_code)
    elif args.command == 'verify':
        exit_code = verify_manifest(Path(args.path), Path(args.manifest))
        exit(exit_code)

if __name__ == '__main__':
    main()
