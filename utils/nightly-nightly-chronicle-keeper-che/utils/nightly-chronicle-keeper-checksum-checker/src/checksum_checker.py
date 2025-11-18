import hashlib
import sys
import os

def calculate_checksum(filepath: str) -> str:
    """Calculates the SHA256 checksum for a given file."""
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

def verify_checksum(filepath: str, expected_checksum: str) -> bool:
    """Verifies a file's checksum against an expected value."""
    actual_checksum = calculate_checksum(filepath)
    if actual_checksum == expected_checksum:
        return True
    return False

def main():
    if len(sys.argv) < 3:
        print("Usage:", file=sys.stderr)
        print("  python src/checksum_checker.py generate <filepath>", file=sys.stderr)
        print("  python src/checksum_checker.py verify <filepath> <expected_checksum>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if command == "generate":
        checksum = calculate_checksum(filepath)
        print(f"{checksum} {filepath}")
    elif command == "verify":
        if len(sys.argv) < 4:
            print("Usage: python src/checksum_checker.py verify <filepath> <expected_checksum>", file=sys.stderr)
            sys.exit(1)
        expected_checksum = sys.argv[3]
        if verify_checksum(filepath, expected_checksum):
            print(f"Verification successful for {filepath}")
        else:
            actual_checksum = calculate_checksum(filepath) # Recalculate to show actual
            print(f"Verification failed for {filepath}. Expected: {expected_checksum}, Got: {actual_checksum}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
