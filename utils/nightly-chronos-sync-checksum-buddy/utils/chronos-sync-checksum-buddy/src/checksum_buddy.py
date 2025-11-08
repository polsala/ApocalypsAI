import argparse
import hashlib
import os
import sys

def calculate_checksum(file_path: str, algorithm: str) -> str:
    """Calculates the checksum of a file using the specified algorithm."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser(
        description="Chronos-Sync Checksum Buddy: Generate and verify file checksums."
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a checksum for a file.')
    generate_parser.add_argument('--file', required=True, help='Path to the file.')
    generate_parser.add_argument('--algorithm', default='sha256', choices=['sha256', 'md5'],
                                   help='Checksum algorithm (default: sha256).')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify a file against an expected checksum.')
    verify_parser.add_argument('--file', required=True, help='Path to the file.')
    verify_parser.add_argument('--expected-checksum', required=True, help='The expected checksum value.')
    verify_parser.add_argument('--algorithm', default='sha256', choices=['sha256', 'md5'],
                                 help='Checksum algorithm (default: sha256).')

    args = parser.parse_args()

    try:
        if args.command == 'generate':
            checksum = calculate_checksum(args.file, args.algorithm)
            print(f"Checksum ({args.algorithm.upper()}): {checksum}")
        elif args.command == 'verify':
            actual_checksum = calculate_checksum(args.file, args.algorithm)
            if actual_checksum == args.expected_checksum:
                print("Checksum MATCHES!")
                sys.exit(0)
            else:
                print(f"Checksum MISMATCH! Expected: {args.expected_checksum}, Got: {actual_checksum}")
                sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
