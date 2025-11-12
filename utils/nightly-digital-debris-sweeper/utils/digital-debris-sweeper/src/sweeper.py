import os
import sys

def find_digital_debris(paths):
    """
    Scans the given paths for digital debris such as empty directories,
    common orphaned metadata files, and cache directories.

    Args:
        paths (list): A list of directory paths to scan.

    Returns:
        list: A list of strings, each describing a piece of debris found.
    """
    debris_found = []
    
    # Define common debris patterns
    ORPHANED_METADATA_FILES = ['.DS_Store', 'Thumbs.db', 'desktop.ini']
    CACHE_DIRS = ['__pycache__']
    TEMP_FILE_EXTENSIONS = ['.tmp', '.log', '.bak'] # Simple check for common temp extensions

    for base_path in paths:
        if not os.path.isdir(base_path):
            print(f"Warning: Path '{base_path}' is not a directory or does not exist. Skipping.", file=sys.stderr)
            continue

        print(f"🧹 Scanning {base_path} for digital debris...")

        for root, dirs, files in os.walk(base_path):
            # Check for empty directories
            if not dirs and not files and root != base_path: # Don't report the base path itself as empty
                debris_found.append(f"Empty Directory: {root}")

            # Check for orphaned metadata files
            for file_name in files:
                if file_name in ORPHANED_METADATA_FILES:
                    debris_found.append(f"Orphaned Metadata: {os.path.join(root, file_name)}")
                elif any(file_name.endswith(ext) for ext in TEMP_FILE_EXTENSIONS):
                    # Simple check for temp files, could be more sophisticated
                    debris_found.append(f"Temporary File: {os.path.join(root, file_name)}")

            # Check for cache directories
            for dir_name in dirs:
                if dir_name in CACHE_DIRS:
                    debris_found.append(f"Cache Directory: {os.path.join(root, dir_name)}")
    
    return debris_found

def main():
    """
    Main entry point for the Digital Debris Sweeper.
    Accepts paths as command-line arguments or scans the current directory.
    """
    scan_paths = sys.argv[1:] if len(sys.argv) > 1 else [os.getcwd()]

    debris = find_digital_debris(scan_paths)

    if debris:
        print("\nIdentified Debris:")
        for item in debris:
            print(f"- {item}")
    else:
        print("\nNo significant digital debris found. Your digital wasteland is surprisingly clean!")

    print("\nScan complete. Your digital wasteland is a little cleaner (in knowledge, at least)!")

if __name__ == "__main__":
    main()
