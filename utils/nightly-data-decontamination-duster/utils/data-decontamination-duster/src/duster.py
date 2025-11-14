import os
import shutil
import argparse
from typing import List, Tuple

def find_irradiated_data(paths_to_scan: List[str]) -> List[Tuple[str, int]]:
    """
    Scans specified paths for files/directories to be 'decontaminated'.
    Returns a list of (path, size_in_bytes) tuples.
    """
    found_items = []
    for path_pattern in paths_to_scan:
        # For simplicity, this version checks if the path exists directly.
        # A more advanced version might include globbing or regex matching.
        if os.path.exists(path_pattern):
            if os.path.isfile(path_pattern):
                found_items.append((path_pattern, os.path.getsize(path_pattern)))
            elif os.path.isdir(path_pattern):
                # Recursively calculate directory size
                dir_size = 0
                for dirpath, dirnames, filenames in os.walk(path_pattern):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if not os.path.islink(fp): # Avoid symlink loops
                            try:
                                dir_size += os.path.getsize(fp)
                            except OSError: # Handle permission errors for files
                                pass
                found_items.append((path_pattern, dir_size))
    return found_items

def decontaminate_data(items_to_remove: List[str], dry_run: bool = True) -> List[str]:
    """
    Removes the specified items. Returns a list of successfully removed items.
    """
    removed_items = []
    for item_path in items_to_remove:
        if dry_run:
            print(f"[DRY RUN] Would decontaminate: {item_path}")
            removed_items.append(item_path) # For dry run, consider it "removed" for reporting
            continue

        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                removed_items.append(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                removed_items.append(item_path)
            else:
                print(f"Warning: {item_path} is neither a file nor a directory. Skipping.")
        except OSError as e:
            print(f"Error decontaminating {item_path}: {e}")
    return removed_items

def format_size(size_bytes: int) -> str:
    """Formats bytes into human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB" # Should be enough for apocalypse

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Data Decontamination Duster: Cleanse your system of digital fallout."
    )
    parser.add_argument(
        "paths",
        nargs=":", # Allow 0 or more paths, but require at least one for meaningful operation
        default=[],
        help="One or more paths (files or directories) to scan for 'irradiated' data."
    )
    parser.add_argument(
        "--cleanse",
        action="store_true",
        help="Perform actual decontamination (delete files/directories). Default is dry run."
    )
    args = parser.parse_args()

    if not args.paths:
        print("Error: Please provide at least one path to scan. Use `python src/duster.py --help` for usage.")
        exit(1)

    print("\n--- ApocalypsAI Data Decontamination Duster ---")
    print("Scanning for irradiated data...")

    irradiated_items = find_irradiated_data(args.paths)

    if not irradiated_items:
        print("No irradiated data detected. Your system is pristine... for now.")
        return

    total_size = sum(item[1] for item in irradiated_items)
    print(f"\nDetected {len(irradiated_items)} irradiated data clusters, totaling {format_size(total_size)}:")
    for path, size in irradiated_items:
        print(f"  - {path} ({format_size(size)})")

    if args.cleanse:
        print("\nInitiating decontamination sequence...")
        removed_items = decontaminate_data([item[0] for item in irradiated_items], dry_run=False)
        # Recalculate removed size based on actually removed items
        removed_size = sum(item[1] for item in irradiated_items if item[0] in removed_items)
        print(f"\nDecontamination complete. {len(removed_items)} clusters purged, reclaiming {format_size(removed_size)} of digital wasteland.")
    else:
        print("\nDry run complete. To perform actual decontamination, run with --cleanse.")
        decontaminate_data([item[0] for item in irradiated_items], dry_run=True) # Show dry run output

if __name__ == "__main__":
    main()
