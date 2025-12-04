import os
import sys
import hashlib
import argparse
import shutil


def hash_file(path, blocksize=65536):
    """Return the SHA‑256 hash of the file at *path*.

    The function reads the file in chunks to avoid loading large files into memory.
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hasher.update(block)
    return hasher.hexdigest()


def find_duplicates(root):
    """Scan *root* recursively and return a dict mapping file hash to a list of duplicate paths.

    The algorithm first groups files by size to reduce the number of hash calculations.
    """
    size_map = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(fpath)
            except OSError:
                continue
            size_map.setdefault(size, []).append(fpath)

    duplicates = {}
    for size, paths in size_map.items():
        if len(paths) < 2:
            continue
        hash_map = {}
        for p in paths:
            h = hash_file(p)
            hash_map.setdefault(h, []).append(p)
        for h, dup_paths in hash_map.items():
            if len(dup_paths) > 1:
                duplicates[h] = dup_paths
    return duplicates


def delete_duplicates(duplicates, dry_run=False):
    """Delete all but the first file in each duplicate group.

    Parameters
    ----------
    duplicates : dict
        Mapping of hash to list of file paths.
    dry_run : bool
        If True, print actions without deleting.
    """
    for h, paths in duplicates.items():
        keep = paths[0]
        for dup in paths[1:]:
            if dry_run:
                print(f"[DRY-RUN] Would delete {dup}")
            else:
                os.remove(dup)
                print(f"Deleted {dup}")


def move_duplicates(duplicates, target_dir, dry_run=False):
    """Move all but the first file in each duplicate group to *target_dir*.

    Parameters
    ----------
    duplicates : dict
        Mapping of hash to list of file paths.
    target_dir : str
        Destination directory for moved duplicates.
    dry_run : bool
        If True, print actions without moving.
    """
    os.makedirs(target_dir, exist_ok=True)
    for h, paths in duplicates.items():
        for dup in paths[1:]:
            dest = os.path.join(target_dir, os.path.basename(dup))
            if dry_run:
                print(f"[DRY-RUN] Would move {dup} to {dest}")
            else:
                shutil.move(dup, dest)
                print(f"Moved {dup} to {dest}")


def report_duplicates(duplicates):
    """Print a human‑readable report of duplicate groups."""
    for h, paths in duplicates.items():
        print(f"Hash: {h}")
        for p in paths:
            print(f"  {p}")


def main():
    parser = argparse.ArgumentParser(description="File deduplicator utility")
    parser.add_argument("--root", required=True, help="Root directory to scan")
    parser.add_argument(
        "--action",
        choices=["report", "delete", "move"],
        default="report",
        help="Action to perform",
    )
    parser.add_argument("--target-dir", help="Target directory for move action")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without performing")
    args = parser.parse_args()

    duplicates = find_duplicates(args.root)
    if not duplicates:
        print("No duplicates found.")
        sys.exit(0)

    if args.action == "report":
        report_duplicates(duplicates)
    elif args.action == "delete":
        delete_duplicates(duplicates, dry_run=args.dry_run)
    elif args.action == "move":
        if not args.target_dir:
            print("Error: --target-dir required for move action")
            sys.exit(1)
        move_duplicates(duplicates, args.target_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
