import os
import hashlib
import json
import sys

def calculate_sha256(filepath):
    """Calculates the SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string in chunks
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        return None # File not found or unreadable

def generate_manifest(directory_path, output_manifest_path):
    """
    Generates a SHA256 checksum manifest for all files in a given directory.
    The manifest is a JSON file mapping relative file paths to their checksums.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.", file=sys.stderr)
        return 1

    manifest = {}
    # +1 for the trailing slash/separator
    base_path_len = len(directory_path) + len(os.sep) if not directory_path.endswith(os.sep) else len(directory_path)

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Get path relative to the base directory
            # Ensure consistent path separators for manifest keys
            relative_path = os.path.relpath(filepath, directory_path).replace(os.sep, '/')
            
            checksum = calculate_sha256(filepath)
            if checksum:
                manifest[relative_path] = checksum
            else:
                print(f"Warning: Could not calculate checksum for '{filepath}'. Skipping.", file=sys.stderr)

    try:
        with open(output_manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)
        print(f"Manifest generated successfully at '{output_manifest_path}' for directory '{directory_path}'.")
        return 0
    except IOError as e:
        print(f"Error: Could not write manifest to '{output_manifest_path}': {e}", file=sys.stderr)
        return 1

def verify_manifest(directory_path, manifest_path):
    """
    Verifies files in a directory against an existing checksum manifest.
    Reports missing files, new files, and files with altered checksums.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.", file=sys.stderr)
        return 1
    if not os.path.isfile(manifest_path):
        print(f"Error: Manifest file '{manifest_path}' not found.", file=sys.stderr)
        return 1

    try:
        with open(manifest_path, 'r') as f:
            expected_manifest = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in manifest file '{manifest_path}'.", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"Error: Could not read manifest file '{manifest_path}': {e}", file=sys.stderr)
        return 1

    current_manifest = {}
    
    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, directory_path).replace(os.sep, '/')
            checksum = calculate_sha256(filepath)
            if checksum:
                current_manifest[relative_path] = checksum
            else:
                print(f"Warning: Could not calculate checksum for current file '{filepath}'. Skipping.", file=sys.stderr)

    # Compare manifests
    issues_found = False

    # Check for missing or altered files
    for relative_path, expected_checksum in expected_manifest.items():
        if relative_path not in current_manifest:
            print(f"MISSING: File '{relative_path}' is missing from '{directory_path}'.")
            issues_found = True
        elif current_manifest[relative_path] != expected_checksum:
            print(f"ALTERED: Checksum mismatch for '{relative_path}'. Expected '{expected_checksum}', got '{current_manifest[relative_path]}'.")
            issues_found = True

    # Check for new files
    for relative_path in current_manifest:
        if relative_path not in expected_manifest:
            print(f"NEW: File '{relative_path}' found in '{directory_path}' but not in manifest.")
            issues_found = True

    if not issues_found:
        print(f"Verification successful: All files in '{directory_path}' match the manifest '{manifest_path}'.")
        return 0
    else:
        print(f"Verification completed with issues for '{directory_path}' against '{manifest_path}'.")
        return 1

def main():
    if len(sys.argv) < 3:
        print("Usage:", file=sys.stderr)
        print("  python src/checksum_calculator.py generate <path_to_directory> [output_manifest_path]", file=sys.stderr)
        print("  python src/checksum_calculator.py verify <path_to_directory> <path_to_manifest>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "generate":
        directory_path = sys.argv[2]
        output_manifest_path = sys.argv[3] if len(sys.argv) > 3 else "checksum_manifest.json"
        sys.exit(generate_manifest(directory_path, output_manifest_path))
    elif command == "verify":
        directory_path = sys.argv[2]
        manifest_path = sys.argv[3]
        sys.exit(verify_manifest(directory_path, manifest_path))
    else:
        print(f"Error: Unknown command '{command}'. Use 'generate' or 'verify'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
