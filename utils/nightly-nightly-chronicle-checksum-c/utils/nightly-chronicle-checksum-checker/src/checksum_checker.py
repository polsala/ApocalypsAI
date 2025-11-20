import hashlib
import argparse
import os
import sys

def calculate_checksum(filepath: str) -> str:
    """Calculates the SHA256 checksum of a given file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):  # Read in 8KB chunks
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

def generate_checksum_file(filepath: str):
    """Generates a .sha256 file for the given file."""
    checksum = calculate_checksum(filepath)
    checksum_filepath = f"{filepath}.sha256"
    try:
        with open(checksum_filepath, 'w') as f:
            f.write(f"{checksum}  {os.path.basename(filepath)}\n")
        print(f"Checksum generated for '{filepath}' and saved to '{checksum_filepath}'")
    except IOError as e:
        print(f"Error writing checksum file '{checksum_filepath}': {e}", file=sys.stderr)
        sys.exit(1)

def verify_checksum_file(filepath: str) -> bool:
    """Verifies a file against its .sha256 checksum file."""
    checksum_filepath = f"{filepath}.sha256"

    if not os.path.exists(checksum_filepath):
        print(f"Error: Checksum file not found at '{checksum_filepath}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(checksum_filepath, 'r') as f:
            line = f.readline().strip()
            if not line:
                print(f"Error: Checksum file '{checksum_filepath}' is empty or malformed.", file=sys.stderr)
                sys.exit(1)
            parts = line.split('  ', 1) # Split only on the first '  '
            if len(parts) != 2:
                print(f"Error: Checksum file '{checksum_filepath}' has an invalid format.", file=sys.stderr)
                sys.exit(1)
            expected_checksum, expected_filename = parts
            
            if os.path.basename(filepath) != expected_filename:
                print(f"Warning: Filename in checksum file ('{expected_filename}') does not match provided file ('{os.path.basename(filepath)}'). Proceeding with checksum verification.", file=sys.stderr)

    except IOError as e:
        print(f"Error reading checksum file '{checksum_filepath}': {e}", file=sys.stderr)
        sys.exit(1)

    actual_checksum = calculate_checksum(filepath)

    if actual_checksum == expected_checksum:
        print(f"Integrity check PASSED for '{filepath}'.")
        return True
    else:
        print(f"Integrity check FAILED for '{filepath}'.")
        print(f"  Expected: {expected_checksum}")
        print(f"  Actual:   {actual_checksum}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Checksum Checker: Generate and verify SHA256 checksums for files."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a .sha256 checksum file for a given file.')
    generate_parser.add_argument('filepath', type=str, help='Path to the file for which to generate a checksum.')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a file against its .sha256 checksum file.')
    verify_parser.add_argument('filepath', type=str, help='Path to the file to verify.')

    args = parser.parse_args()

    if args.command == 'generate':
        generate_checksum_file(args.filepath)
    elif args.command == 'verify':
        if not verify_checksum_file(args.filepath):
            sys.exit(1) # Exit with error code if verification fails

if __name__ == '__main__':
    main()
