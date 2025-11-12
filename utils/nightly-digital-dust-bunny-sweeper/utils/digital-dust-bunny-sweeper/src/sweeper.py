import os
import hashlib
import time
import argparse
from datetime import datetime, timedelta

class DigitalDustBunnySweeper:
    def __init__(self, root_dir, age_threshold_days=365):
        self.root_dir = root_dir
        self.age_threshold_days = age_threshold_days
        self.empty_files = []
        self.duplicate_files = {} # hash -> [paths]
        self.old_files = []
        self.now = time.time()
        self.age_threshold_timestamp = self.now - (age_threshold_days * 24 * 3600)

    def _get_file_hash(self, filepath, block_size=65536):
        """Calculates SHA256 hash of a file."""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            return hasher.hexdigest()
        except IOError:
            return None # Handle unreadable files

    def scan(self):
        if not os.path.isdir(self.root_dir):
            print(f"Error: Directory '{self.root_dir}' not found.")
            return

        print(f"Scanning '{self.root_dir}' for digital dust bunnies...")

        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if not os.path.islink(filepath): # Skip symlinks to avoid issues
                    try:
                        file_size = os.path.getsize(filepath)
                        file_mtime = os.path.getmtime(filepath)

                        # Check for empty files
                        if file_size == 0:
                            self.empty_files.append(filepath)

                        # Check for old files
                        if file_mtime < self.age_threshold_timestamp:
                            self.old_files.append(filepath)

                        # Check for duplicate files (only if not empty)
                        if file_size > 0:
                            file_hash = self._get_file_hash(filepath)
                            if file_hash:
                                self.duplicate_files.setdefault(file_hash, []).append(filepath)

                    except OSError as e:
                        print(f"Warning: Could not process '{filepath}': {e}")

    def report(self, dry_run=True):
        print("\n--- Digital Dust Bunny Report ---")
        print(f"Scan conducted on: {datetime.fromtimestamp(self.now).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Age threshold for 'old' files: {self.age_threshold_days} days\n")

        total_bunnies = 0

        if self.empty_files:
            print("### Empty Files (0 bytes) ###")
            for f in self.empty_files:
                print(f"- {f}")
                total_bunnies += 1
            print(f"Found {len(self.empty_files)} empty files.\n")

        duplicates_found = {h: paths for h, paths in self.duplicate_files.items() if len(paths) > 1}
        if duplicates_found:
            print("### Duplicate Files (identical content) ###")
            for file_hash, paths in duplicates_found.items():
                print(f"  Hash: {file_hash[:10]}...")
                for p in paths:
                    print(f"  - {p}")
                total_bunnies += len(paths) - 1 # Count only the redundant ones
            print(f"Found {sum(len(paths) - 1 for paths in duplicates_found.values())} redundant duplicate files.\n")

        if self.old_files:
            print(f"### Old Files (modified before {datetime.fromtimestamp(self.age_threshold_timestamp).strftime('%Y-%m-%d')}) ###")
            for f in self.old_files:
                print(f"- {f} (Modified: {datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d')})")
                total_bunnies += 1
            print(f"Found {len(self.old_files)} old files.\n")

        if total_bunnies == 0:
            print("No digital dust bunnies found. Your directory is sparkling clean!")
        else:
            print(f"Total potential digital dust bunnies to clean: {total_bunnies}")
            if dry_run:
                print("\nThis was a DRY RUN. No files were deleted.")
                print("To actually delete files, run with '--action delete' (USE WITH CAUTION!).")
            else:
                print("\nFiles were deleted (not implemented in this version, for safety).")
                print("This version only reports. Manual deletion is required.")

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for 'digital dust bunnies' (empty, old, or duplicate files)."
    )
    parser.add_argument(
        "directory",
        help="The root directory to scan."
    )
    parser.add_argument(
        "--age-threshold",
        type=int,
        default=365,
        help="Files older than this many days will be flagged as 'old'. Default: 365 days."
    )
    parser.add_argument(
        "--action",
        choices=["report", "delete"],
        default="report",
        help="Action to perform. 'report' (default) shows findings. 'delete' (NOT IMPLEMENTED FOR SAFETY) would remove them."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run (default for 'report' action). No files will be deleted."
    )

    args = parser.parse_args()

    # Force dry_run if action is report, or if dry_run is explicitly set
    is_dry_run = args.dry_run or args.action == "report"

    if args.action == "delete":
        print("Warning: The 'delete' action is not implemented for safety in this version.")
        print("This utility will only report findings. Please review and delete manually.")
        is_dry_run = True # Always dry run for now

    sweeper = DigitalDustBunnySweeper(args.directory, args.age_threshold)
    sweeper.scan()
    sweeper.report(dry_run=is_dry_run)

if __name__ == "__main__":
    main()
