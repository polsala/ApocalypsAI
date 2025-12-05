import os
import hashlib
import argparse
import sys

def calculate_sha256(filepath):
    """Calculates the SHA256 checksum of a given file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def generate_checksums(directory):
    """Generates a dictionary of {filepath: sha256_checksum} for all files in a directory."""
    checksums = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            checksum = calculate_sha256(filepath)
            if checksum:
                checksums[filepath] = checksum
    return checksums

def load_manifest(manifest_path):
    """Loads checksums from a manifest file."""
    manifest = {}
    if not os.path.exists(manifest_path):
        return manifest
    try:
        with open(manifest_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' ', 1) # Split only on the first space
                if len(parts) == 2:
                    checksum, filepath = parts
                    manifest[filepath] = checksum
                else:
                    print(f"Warning: Malformed line in manifest: {line}", file=sys.stderr)
        return manifest
    except IOError as e:
        print(f"Error reading manifest file {manifest_path}: {e}", file=sys.stderr)
        return {}

def save_manifest(manifest_path, checksums):
    """Saves checksums to a manifest file."""
    try:
        # Ensure the directory for the manifest file exists
        os.makedirs(os.path.dirname(manifest_path) or '.', exist_ok=True)
        with open(manifest_path, 'w') as f:
            for filepath, checksum in sorted(checksums.items()):
                f.write(f"{checksum} {filepath}\n")
        print(f"Manifest saved to {manifest_path}")
    except IOError as e:
        print(f"Error writing manifest file {manifest_path}: {e}", file=sys.stderr)

def verify_checksums(directory, manifest_path):
    """Verifies current file checksums against a stored manifest."""
    print("--- Checksum Guardian Report ---")

    old_checksums = load_manifest(manifest_path)
    current_checksums = generate_checksums(directory)

    added_files = []
    removed_files = []
    modified_files = []
    unchanged_count = 0

    # Check for modified or unchanged files
    for filepath, current_checksum in current_checksums.items():
        if filepath in old_checksums:
            if old_checksums[filepath] != current_checksum:
                modified_files.append((filepath, old_checksums[filepath], current_checksum))
            else:
                unchanged_count += 1
        else:
            added_files.append(filepath)

    # Check for removed files
    for filepath in old_checksums:
        if filepath not in current_checksums:
            removed_files.append(filepath)

    if added_files:
        print("\nFiles Added:")
        for f in added_files:
            print(f"  - {f}")
    else:
        print("\nNo new files detected.")

    if removed_files:
        print("\nFiles Removed:")
        for f in removed_files:
            print(f"  - {f}")
    else:
        print("\nNo files removed.")

    if modified_files:
        print("\nFiles Modified:")
        for f, old_c, new_c in modified_files:
            print(f"  - {f} (Old: {old_c[:7]}..., New: {new_c[:7]}...)")
    else:
        print("\nNo files modified.")

    print(f"\nFiles Unchanged: {unchanged_count}")
    print("\n--- Report End ---")

    # Return True if no changes, False if changes detected
    return not (added_files or removed_files or modified_files)

def main():
    parser = argparse.ArgumentParser(description="Nightly Checksum Guardian: Monitor file integrity.")
    parser.add_argument('--path', required=True, help='The directory to monitor for file changes.')
    parser.add_argument('--manifest', required=True, help='The path to the checksum manifest file.')

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.manifest):
        print(f"Manifest file '{args.manifest}' not found. Generating new manifest...")
        current_checksums = generate_checksums(args.path)
        if current_checksums:
            save_manifest(args.manifest, current_checksums)
            print("Initial manifest generated. Run again to verify.")
        else:
            print(f"No files found in '{args.path}' to generate a manifest.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Manifest file '{args.manifest}' found. Verifying integrity...")
        is_clean = verify_checksums(args.path, args.manifest)
        if is_clean:
            print("All files are intact and unchanged.")
        else:
            print("Integrity check completed with detected changes.")

if __name__ == '__main__':
    main()
