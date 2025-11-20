import os
import hashlib
import json
import argparse

def calculate_file_checksum(filepath, algorithm='sha256'):
    """Calculates the checksum of a single file."""
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error calculating checksum for {filepath}: {e}")
        return None

def calculate_directory_checksums(directory, algorithm='sha256'):
    """Calculates checksums for all files in a directory and its subdirectories."""
    checksums = {}
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return {}

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            # Create a relative path for the manifest
            relative_path = os.path.relpath(filepath, directory)
            checksum = calculate_file_checksum(filepath, algorithm)
            if checksum:
                checksums[relative_path] = checksum
    return checksums

def save_checksums(checksums, output_file):
    """Saves a dictionary of checksums to a JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(checksums, f, indent=4)
        print(f"Checksums saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving checksums to {output_file}: {e}")
        return False

def load_checksums(input_file):
    """Loads a dictionary of checksums from a JSON file."""
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Manifest file not found: {input_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in manifest file: {input_file}")
        return None
    except Exception as e:
        print(f"Error loading checksums from {input_file}: {e}")
        return None

def verify_checksums(directory, saved_checksums, algorithm='sha256'):
    """Verifies current directory checksums against saved ones."""
    if not saved_checksums:
        print("No saved checksums to verify against.")
        return False

    current_checksums = calculate_directory_checksums(directory, algorithm)

    all_ok = True
    print("\n--- Verification Report ---")

    # Check for changed or missing files
    for relative_path, saved_checksum in saved_checksums.items():
        if relative_path not in current_checksums:
            print(f"[MISSING] {relative_path} (was in manifest, but not found now)")
            all_ok = False
        elif current_checksums[relative_path] != saved_checksum:
            print(f"[CHANGED] {relative_path} (checksum mismatch)")
            all_ok = False
        else:
            print(f"[OK]      {relative_path}")

    # Check for new files
    for relative_path in current_checksums:
        if relative_path not in saved_checksums:
            print(f"[NEW]     {relative_path} (not in manifest)")
            all_ok = False

    print("---------------------------")
    if all_ok:
        print("All files verified successfully. Integrity maintained!")
    else:
        print("Integrity check failed. Discrepancies found.")
    return all_ok

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper Checksum Calculator: Calculate and verify file integrity."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Calculate command
    calculate_parser = subparsers.add_parser('calculate', help='Calculate checksums for a directory.')
    calculate_parser.add_argument('--directory', required=True, help='Path to the directory to checksum.')
    calculate_parser.add_argument('--output', required=True, help='Output JSON file for checksums.')
    calculate_parser.add_argument('--algorithm', default='sha256', help='Hashing algorithm (e.g., sha256, md5).')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify checksums against a manifest.')
    verify_parser.add_argument('--directory', required=True, help='Path to the directory to verify.')
    verify_parser.add_argument('--manifest', required=True, help='Path to the JSON manifest file.')
    verify_parser.add_argument('--algorithm', default='sha256', help='Hashing algorithm (e.g., sha256, md5).')

    args = parser.parse_args()

    if args.command == 'calculate':
        checksums = calculate_directory_checksums(args.directory, args.algorithm)
        if checksums:
            save_checksums(checksums, args.output)
    elif args.command == 'verify':
        saved_checksums = load_checksums(args.manifest)
        if saved_checksums is not None:
            verify_checksums(args.directory, saved_checksums, args.algorithm)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
