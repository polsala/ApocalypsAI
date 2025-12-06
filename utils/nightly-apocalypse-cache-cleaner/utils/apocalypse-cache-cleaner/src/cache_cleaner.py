import os
import shutil
import argparse
import sys

# List of common cache/build directory patterns to look for
CACHE_PATTERNS = [
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '.venv',
    'venv',
    'node_modules',
    'dist',
    'build',
    'target',
    'out',
    'tmp'
]

def get_dir_size(path):
    """Calculates the total size of a directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_bytes(size):
    """Formats bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def find_and_clean_caches(root_dir, delete_mode=False):
    """Finds cache directories and optionally deletes them."""
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.")
        return

    print(f"Scanning '{root_dir}' for digital debris...")
    found_caches = []

    for dirpath, dirnames, _ in os.walk(root_dir):
        # Make a copy of dirnames to allow modification during iteration
        # This is crucial to prevent os.walk from descending into deleted/ignored dirs
        dirnames_copy = list(dirnames)
        for dname in dirnames_copy:
            if dname.lower() in CACHE_PATTERNS:
                full_path = os.path.join(dirpath, dname)
                size = get_dir_size(full_path)
                found_caches.append({'path': full_path, 'size': size})
                
                # Prevent os.walk from descending into this cache directory
                # by removing it from the list of directories to visit.
                if dname in dirnames:
                    dirnames.remove(dname)

    if not found_caches:
        print("No digital debris found. Your project is lean and mean!")
        return

    total_reclaimable_size = sum(cache['size'] for cache in found_caches)

    print("\n--- Digital Debris Report ---")
    for cache in found_caches:
        print(f"  - {cache['path']} ({format_bytes(cache['size'])})")
    print(f"\nTotal reclaimable space: {format_bytes(total_reclaimable_size)}")

    if delete_mode:
        confirm = input("\nProceed with deletion of all identified caches? (y/N): ").lower()
        if confirm == 'y':
            print("Initiating digital resource conservation protocol...")
            for cache in found_caches:
                try:
                    shutil.rmtree(cache['path'])
                    print(f"  Deleted: {cache['path']}")
                except OSError as e:
                    print(f"  Error deleting {cache['path']}: {e}")
            print("Digital resources conserved. Stay vigilant!")
        else:
            print("Deletion aborted. Digital debris remains. Proceed with caution.")
    else:
        print("\nRun with '--delete' to reclaim this space.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Apocalypse Cache Cleaner: Conserve digital resources by cleaning project caches."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan for cache files."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If set, prompts for confirmation to delete identified cache directories."
    )

    args = parser.parse_args()
    find_and_clean_caches(args.path, args.delete)
