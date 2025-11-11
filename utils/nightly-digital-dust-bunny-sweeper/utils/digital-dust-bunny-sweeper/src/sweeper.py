import os
import argparse
import sys

def is_empty_dir(path):
    """Checks if a directory is empty (contains no files or subdirectories)."""
    if not os.path.isdir(path):
        return False
    return not os.listdir(path)

def is_log_or_temp_file(filename):
    """Checks if a file matches common log/temp/backup patterns."""
    name_lower = filename.lower()
    return any(name_lower.endswith(ext) for ext in ['.log', '.tmp', '.bak', '.swp', '.temp'])

def is_build_artifact(path, filename):
    """Checks if a file or directory matches common build artifact or OS junk patterns."""
    # Common OS junk files
    if filename in ['.DS_Store', 'Thumbs.db']:
        return True

    # Common Python build artifacts
    if filename == '__pycache__':
        return True

    # Common build output directories (relative to the scan root, or just by name)
    if os.path.isdir(path):
        dir_name = os.path.basename(path)
        if dir_name in ['build', 'dist', 'target', '.venv', 'env']:
            return True

    return False

def find_dust_bunnies(root_dir):
    """Scans the root_dir for digital dust bunnies and returns a list of paths."""
    dust_bunnies = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False): # topdown=False for empty dir check
        # Check for empty directories first (bottom-up)
        if is_empty_dir(dirpath):
            dust_bunnies.append(('[EMPTY DIR]', dirpath))

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if is_log_or_temp_file(filename):
                dust_bunnies.append(('[LOG/TEMP FILE]', file_path))
            elif is_build_artifact(file_path, filename):
                dust_bunnies.append(('[BUILD ARTIFACT]', file_path))

        for dirname in dirnames:
            dir_full_path = os.path.join(dirpath, dirname)
            if is_build_artifact(dir_full_path, dirname):
                # Add the entire build directory as a dust bunny
                dust_bunnies.append(('[BUILD ARTIFACT DIR]', dir_full_path))

    # Filter out duplicates (e.g., if an empty dir was also a build artifact dir, it might be listed twice)
    unique_bunnies = []
    seen_paths = set()
    for bunny_type, bunny_path in dust_bunnies:
        if bunny_path not in seen_paths:
            unique_bunnies.append((bunny_type, bunny_path))
            seen_paths.add(bunny_path)

    return unique_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for 'digital dust bunnies' (empty dirs, logs, temp files, build artifacts)."
    )
    parser.add_argument(
        'path', 
        type=str, 
        help='The root directory to scan.'
    )

    args = parser.parse_args()
    scan_path = os.path.abspath(args.path)

    if not os.path.isdir(scan_path):
        print(f"Error: The provided path '{scan_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {scan_path} for digital dust bunnies...")

    bunnies = find_dust_bunnies(scan_path)

    if not bunnies:
        print("No digital dust bunnies found. Your repository is sparkling clean!")
    else:
        print(f"\nFound {len(bunnies)} digital dust bunnies:")
        for bunny_type, bunny_path in sorted(bunnies, key=lambda x: x[1]): # Sort by path for consistent output
            print(f"- {bunny_type} {bunny_path}")
        print("\nReview the list above. To remove them, you would typically use 'rm -rf' or similar commands manually.")

if __name__ == '__main__':
    main()
