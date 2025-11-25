import os
import sys
import argparse

def delete_empty_dirs(path):
    """
    Recursively deletes empty directories starting from the given path.
    It walks the directory tree from bottom-up to ensure parent directories
    become empty and can be deleted if all their children are gone.
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.", file=sys.stderr)
        return

    deleted_count = 0
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        try:
            # Re-list directory content to be sure, as dirnames/filenames from os.walk
            # might be stale if subdirs were deleted in the same walk iteration.
            current_contents = os.listdir(dirpath)
            if not current_contents:
                print(f"Deleting empty directory: {dirpath}")
                os.rmdir(dirpath)
                deleted_count += 1 # Increment only on successful deletion
        except OSError as e:
            print(f"Warning: Could not delete directory {dirpath}: {e}", file=sys.stderr)

    if deleted_count == 0:
        print(f"No empty directories found under '{path}'.")
    else:
        print(f"Successfully deleted {deleted_count} empty directories under '{path}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies by deleting empty directories."
    )
    parser.add_argument("path", help="The root directory to start sweeping from.")
    args = parser.parse_args()

    delete_empty_dirs(args.path)

if __name__ == "__main__":
    main()
