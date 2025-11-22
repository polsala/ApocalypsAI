import os
import sys
import argparse

def find_empty_dirs(root_dir):
    """Finds all empty directories within a given root_dir."""
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the directory itself is empty (no files and no subdirectories)
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_broken_symlinks(root_dir):
    """Finds all broken symbolic links within a given root_dir."""
    broken_links = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in dirnames + filenames:
            full_path = os.path.join(dirpath, name)
            if os.path.islink(full_path):
                # A symlink is broken if its target does not exist
                if not os.path.exists(full_path):
                    broken_links.append(full_path)
    return broken_links

def sweep_items(items, dry_run=True, item_type="item"):
    """Deletes a list of items or reports them in dry-run mode."""
    if not items:
        print(f"No {item_type}s found to sweep.")
        return

    print(f"\n--- {item_type.capitalize()}s to be swept ({'Dry Run' if dry_run else 'Sweeping'}) ---")
    for item in items:
        print(f"  - {item}")

    if not dry_run:
        print(f"\nAttempting to sweep {len(items)} {item_type}(s)...")
        for item in items:
            try:
                if os.path.isdir(item): # For empty directories
                    os.rmdir(item)
                    print(f"  [SWEPT] Removed empty directory: {item}")
                else: # For broken symlinks (and potentially other files in future)
                    os.remove(item)
                    print(f"  [SWEPT] Removed broken symlink: {item}")
            except OSError as e:
                print(f"  [ERROR] Could not remove {item_type} {item}: {e}")
        print(f"Sweeping complete.")
    else:
        print(f"\n(Dry run complete. No changes were made.)")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies: empty directories and broken symbolic links."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory from which to start scanning."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If present, only report what would be swept, without making changes."
    )

    args = parser.parse_args()
    scan_path = args.path
    dry_run = args.dry_run

    if not os.path.isdir(scan_path):
        print(f"Error: The provided path '{scan_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{scan_path}' for digital dust bunnies...")

    empty_dirs = find_empty_dirs(scan_path)
    sweep_items(empty_dirs, dry_run, item_type="empty directory")

    broken_links = find_broken_symlinks(scan_path)
    sweep_items(broken_links, dry_run, item_type="broken symbolic link")

    if not empty_dirs and not broken_links:
        print("\nNo digital dust bunnies found. Your directory is pristine!")


if __name__ == "__main__":
    main()
