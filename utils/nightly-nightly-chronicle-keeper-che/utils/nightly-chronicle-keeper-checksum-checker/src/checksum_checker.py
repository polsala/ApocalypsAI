import hashlib
import os
import sys

def generate_checksum(filepath: str) -> str:
    """Generates the SHA256 checksum for a given file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def save_checksum(filepath: str, checksum: str, output_manifest: str = None):
    """
    Saves the checksum to a .sha256 file next to the original file,
    or appends to a specified manifest file.
    """
    if output_manifest:
        mode = 'a' if os.path.exists(output_manifest) else 'w'
        with open(output_manifest, mode) as f:
            f.write(f"{checksum}  {filepath}\n")
        print(f"Checksum for '{filepath}' saved to manifest: '{output_manifest}'")
    else:
        checksum_filepath = f"{filepath}.sha256"
        with open(checksum_filepath, 'w') as f:
            f.write(f"{checksum}  {os.path.basename(filepath)}\n")
        print(f"Checksum for '{filepath}' saved to: '{checksum_filepath}'")

def verify_checksum(filepath: str, expected_checksum: str) -> bool:
    """Verifies a file against an expected SHA256 checksum."""
    try:
        actual_checksum = generate_checksum(filepath)
        if actual_checksum == expected_checksum:
            print(f"Verification successful for '{filepath}'. Checksum matches.")
            return True
        else:
            print(f"Verification FAILED for '{filepath}'. Expected: {expected_checksum}, Actual: {actual_checksum}")
            return False
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python checksum_checker.py generate <filepath> [--manifest <manifest_file>]")
        print("  python checksum_checker.py verify <filepath> <expected_checksum>")
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if command == "generate":
        try:
            checksum = generate_checksum(filepath)
            print(f"Generated SHA256 for '{filepath}': {checksum}")
            if "--manifest" in sys.argv:
                manifest_index = sys.argv.index("--manifest")
                if manifest_index + 1 < len(sys.argv):
                    manifest_file = sys.argv[manifest_index + 1]
                    save_checksum(filepath, checksum, manifest_file)
                else:
                    print("Error: --manifest requires a file path.")
                    sys.exit(1)
            else:
                save_checksum(filepath, checksum)
            sys.exit(0)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
    elif command == "verify":
        if len(sys.argv) < 4:
            print("Usage: python checksum_checker.py verify <filepath> <expected_checksum>")
            sys.exit(1)
        expected_checksum = sys.argv[3]
        if verify_checksum(filepath, expected_checksum):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
