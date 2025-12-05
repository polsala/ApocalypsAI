import argparse
import hashlib
import json
import os
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
    except FileNotFoundError:
        return None # Indicate file not found
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def generate_checksums(directory, output_file):
    """
    Generates a JSON manifest of SHA256 checksums for all files in a directory.
    The manifest maps relative file paths to their checksums.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.", file=sys.stderr)
        return 1

    checksums = {}
    base_path_len = len(directory) + len(os.sep) # For relative paths

    print(f"Generating checksums for '{directory}'...")
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_filepath = filepath[base_path_len:] if filepath.startswith(directory + os.sep) else filename
            
            checksum = calculate_sha256(filepath)
            if checksum:
                checksums[relative_filepath] = checksum
                print(f"  Generated: {relative_filepath}")
            else:
                print(f"  Skipped (error/missing): {relative_filepath}", file=sys.stderr)

    try:
        with open(output_file, "w") as f:
            json.dump(checksums, f, indent=4)
        print(f"\nChecksum manifest saved to '{output_file}'.")
        return 0
    except IOError as e:
        print(f"Error writing manifest file {output_file}: {e}", file=sys.stderr)
        return 1

def verify_checksums(directory, manifest_file):
    """
    Verifies files in a directory against a checksum manifest.
    Reports modified, missing, and new files.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.", file=sys.stderr)
        return 1
    if not os.path.isfile(manifest_file):
        print(f"Error: Manifest file '{manifest_file}' not found.", file=sys.stderr)
        return 1

    try:
        with open(manifest_file, "r") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing manifest file {manifest_file}: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"Error reading manifest file {manifest_file}: {e}", file=sys.stderr)
        return 1

    print(f"Verifying checksums for '{directory}' against '{manifest_file}'...")

    results = {
        "ok": 0,
        "modified": 0,
        "missing": 0,
        "new": 0
    }
    
    # Track files found in directory to identify 'new' files later
    files_in_directory = set()
    base_path_len = len(directory) + len(os.sep) # For relative paths

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_filepath = filepath[base_path_len:] if filepath.startswith(directory + os.sep) else filename
            files_in_directory.add(relative_filepath)

            if relative_filepath in manifest:
                current_checksum = calculate_sha256(filepath)
                if current_checksum is None: # File might have become unreadable
                    print(f"[ERROR] Could not read: {relative_filepath}")
                    results["modified"] += 1 # Treat as modified/problematic
                elif current_checksum == manifest[relative_filepath]:
                    print(f"[OK] {relative_filepath}")
                    results["ok"] += 1
                else:
                    print(f"[MODIFIED] {relative_filepath} (Manifest: {manifest[relative_filepath]}, Current: {current_checksum})")
                    results["modified"] += 1
            else:
                print(f"[NEW] {relative_filepath}")
                results["new"] += 1
    
    # Check for missing files (in manifest but not in directory)
    for relative_filepath in manifest:
        if relative_filepath not in files_in_directory:
            print(f"[MISSING] {relative_filepath}")
            results["missing"] += 1

    print("\n--- Verification Summary ---")
    print(f"OK: {results['ok']}")
    print(f"MODIFIED: {results['modified']}")
    print(f"MISSING: {results['missing']}")
    print(f"NEW: {results['new']}")
    print("----------------------------")

    if results["modified"] > 0 or results["missing"] > 0:
        return 1 # Indicate issues found
    return 0 # All good or only new files

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper Checksum Checker: Generate and verify SHA256 checksums for files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a checksum manifest.")
    generate_parser.add_argument(
        "--directory", "-d", required=True, help="The directory to scan for files."
    )
    generate_parser.add_argument(
        "--output", "-o", required=True, help="The output JSON file for the checksum manifest."
    )

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify files against a checksum manifest.")
    verify_parser.add_argument(
        "--directory", "-d", required=True, help="The directory containing files to verify."
    )
    verify_parser.add_argument(
        "--manifest", "-m", required=True, help="The JSON manifest file to use for verification."
    )

    args = parser.parse_args()

    if args.command == "generate":
        sys.exit(generate_checksums(args.directory, args.output))
    elif args.command == "verify":
        sys.exit(verify_checksums(args.directory, args.manifest))

if __name__ == "__main__":
    main()
