import os
import shutil
import argparse
from typing import List

def is_match(name: str, patterns: List[str]) -> bool:
    """Checks if a file/directory name or extension matches any of the patterns."""
    for pattern in patterns:
        if pattern.startswith('.'):  # Treat as extension
            if name.endswith(pattern):
                return True
        elif name == pattern:  # Treat as exact file/dir name
            return True
    return False

def sweep_debris(root_path: str, patterns: List[str], delete_mode: bool = False) -> List[str]:
    """Scans for and optionally deletes files/directories matching patterns."""
    if not os.path.isdir(root_path):
        print(f"Error: Root path '{root_path}' is not a valid directory.")
        return []

    found_debris = []
    action_word = "Deleting" if delete_mode else "Found"

    print(f"Scanning '{root_path}' for debris matching: {', '.join(patterns)}")
    print(f"Mode: {'Deletion' if delete_mode else 'Dry Run'}")
    print("--------------------------------------------------")

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Check directories first (topdown=True allows modifying dirnames in place)
        dirs_to_remove_from_walk = []
        for dirname in list(dirnames): # Iterate over a copy to allow modification
            full_path = os.path.join(dirpath, dirname)
            if is_match(dirname, patterns):
                found_debris.append(full_path)
                print(f"{action_word} directory: {full_path}")
                if delete_mode:
                    try:
                        shutil.rmtree(full_path)
                        dirs_to_remove_from_walk.append(dirname) # Mark for removal from dirnames
                    except OSError as e:
                        print(f"Error deleting directory {full_path}: {e}")
            
        # Prune dirnames list to prevent os.walk from descending into deleted directories
        for dtr in dirs_to_remove_from_walk:
            dirnames.remove(dtr)

        # Check files
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if is_match(filename, patterns):
                found_debris.append(full_path)
                print(f"{action_word} file: {full_path}")
                if delete_mode:
                    try:
                        os.remove(full_path)
                    except OSError as e:
                        print(f"Error deleting file {full_path}: {e}")

    print("--------------------------------------------------")
    print(f"Scan complete. {len(found_debris)} items {'deleted' if delete_mode else 'identified'}.")
    return found_debris

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sweep away digital debris (temporary files, logs, caches)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory from which to start scanning for debris."
    )
    parser.add_argument(
        "--patterns",
        nargs='+',
        default=[],
        help="A space-separated list of patterns (extensions, filenames, dirnames) to match."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If present, the utility will actually delete the identified debris. (Dry run otherwise)"
    )

    args = parser.parse_args()

    if not args.patterns:
        print("Warning: No patterns provided. Nothing will be swept.")
    else:
        sweep_debris(args.path, args.patterns, args.delete)
