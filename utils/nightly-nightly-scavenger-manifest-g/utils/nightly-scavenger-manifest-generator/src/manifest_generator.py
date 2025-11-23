import os
import hashlib
import argparse
import sys

def human_readable_size(size, decimal_places=1):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0
    return f"{size:.{decimal_places}f} PB" # Just in case of truly massive files

def generate_sha256(filepath, block_size=65536):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(block_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        return "N/A (Read Error)"

def generate_manifest(root_dir, output_file):
    manifest_lines = []
    manifest_lines.append(f"# Scavenger Manifest for {root_dir}\n")
    manifest_lines.append("| Type | Path | Size | SHA256 Hash |")
    manifest_lines.append("|---|---|---|---|")

    # Store all entries to sort them globally for deterministic output
    # (type, full_path, size, hash)
    entries = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Add directories
        for dname in sorted(dirnames):
            full_path = os.path.join(dirpath, dname)
            entries.append(('dir', full_path, '-', '-'))
        
        # Add files
        for fname in sorted(filenames):
            full_path = os.path.join(dirpath, fname)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                hr_size = human_readable_size(size)
                sha256 = generate_sha256(full_path)
                entries.append(('file', full_path, hr_size, sha256))

    # Sort entries for consistent output.
    # Sort by path first, then by type (dir/file) to ensure directories appear before their contents
    entries.sort(key=lambda x: (x[1], x[0]))

    for entry_type, full_path, size, sha256 in entries:
        if entry_type == 'dir':
            manifest_lines.append(f"| Directory | {full_path} | {size} | {sha256} |")
        else: # 'file'
            manifest_lines.append(f"| File | {full_path} | {size} | {sha256} |")

    try:
        with open(output_file, "w") as f:
            f.write("\n".join(manifest_lines))
        print(f"Manifest successfully generated at {output_file}")
        return 0 # Success
    except IOError as e:
        print(f"Error writing manifest to {output_file}: {e}")
        return 1 # Failure

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Markdown manifest of files and directories."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to scan."
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="manifest.md", 
        help="The output Markdown file path. Defaults to manifest.md."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The provided path '{args.path}' is not a valid directory.")
        sys.exit(1)

    exit_code = generate_manifest(args.path, args.output)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
