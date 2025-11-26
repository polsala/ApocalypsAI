import argparse
import hashlib
import json
import os
from typing import Dict, Any

def calculate_sha256(filepath: str, chunk_size: int = 4096) -> str:
    """Calculates the SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return "FILE_NOT_FOUND"
    except Exception as e:
        return f"ERROR: {e}"

def load_manifest(manifest_path: str) -> Dict[str, str]:
    """Loads a checksum manifest from a JSON file."""
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        if not isinstance(manifest, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in manifest.items()):
            raise ValueError("Manifest must be a dictionary of string paths to string checksums.")
        return manifest
    except FileNotFoundError:
        print(f"Error: Manifest file not found at '{manifest_path}'")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in manifest file '{manifest_path}'")
        return {}
    except ValueError as e:
        print(f"Error: Invalid manifest format in '{manifest_path}': {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred loading manifest: {e}")
        return {}

def verify_cache(cache_dir: str, manifest: Dict[str, str]) -> bool:
    """
    Verifies the integrity of files in a cache directory against a manifest.
    Returns True if all files match, False otherwise.
    """
    all_ok = True
    print(f"Verifying cache in '{cache_dir}'...")

    if not os.path.isdir(cache_dir):
        print(f"Error: Cache directory '{cache_dir}' does not exist.")
        return False

    for relative_path, expected_checksum in manifest.items():
        full_path = os.path.join(cache_dir, relative_path)
        print(f"  Checking '{relative_path}'...")

        if not os.path.exists(full_path):
            print(f"    MISSING: File '{relative_path}' not found in cache.")
            all_ok = False
            continue

        actual_checksum = calculate_sha256(full_path)

        if actual_checksum == "FILE_NOT_FOUND": # Should not happen if os.path.exists passed
            print(f"    ERROR: Could not read file '{relative_path}'.")
            all_ok = False
        elif actual_checksum.startswith("ERROR:"):
            print(f"    ERROR: Failed to calculate checksum for '{relative_path}': {actual_checksum}")
            all_ok = False
        elif actual_checksum == expected_checksum:
            print(f"    OK: Checksum matches for '{relative_path}'.")
        else:
            print(f"    CORRUPTED: Checksum mismatch for '{relative_path}'.")
            print(f"      Expected: {expected_checksum}")
            print(f"      Actual:   {actual_checksum}")
            all_ok = False
    
    if not manifest:
        print("Warning: Manifest is empty. No files to verify.")
        return True # Or False, depending on desired behavior for empty manifest. Let's say True if nothing to check.

    return all_ok

def main():
    parser = argparse.ArgumentParser(
        description="Survival Cache Checksum Verifier: Ensures your digital survival caches haven't been corrupted by cosmic rays."
    )
    parser.add_argument(
        "cache_directory",
        help="The path to the directory containing the files to verify."
    )
    parser.add_argument(
        "manifest_file",
        help="The path to the JSON manifest file containing file paths and their expected SHA256 checksums."
    )

    args = parser.parse_args()

    manifest = load_manifest(args.manifest_file)
    if not manifest and os.path.exists(args.manifest_file): # If manifest file exists but is empty/invalid
        print("Verification aborted due to invalid or empty manifest.")
        exit(1)
    elif not manifest and not os.path.exists(args.manifest_file): # If manifest file doesn't exist
        print("Verification aborted as manifest file was not found.")
        exit(1)

    if not verify_cache(args.cache_directory, manifest):
        print("\nVerification FAILED: Some files are missing or corrupted!")
        exit(1)
    else:
        print("\nVerification SUCCESS: All files in the cache are intact!")
        exit(0)

if __name__ == "__main__":
    main()
