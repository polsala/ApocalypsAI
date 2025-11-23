import os
import argparse
import datetime
from pathlib import Path

class CosmicDustBunnyCollector:
    def __init__(self, root_paths, log_age_days=7, dry_run=True):
        self.root_paths = [Path(p).resolve() for p in root_paths]
        self.log_age_days = log_age_days
        self.dry_run = dry_run
        self.dust_bunnies = []
        self.now = datetime.datetime.now()

    def _is_empty_dir(self, path):
        # Mock rationale: In tests, os.listdir is mocked to control directory contents.
        return path.is_dir() and not list(path.iterdir())

    def _is_old_log_file(self, path):
        if path.suffix == '.log' and path.is_file():
            # Mock rationale: datetime.datetime.now and os.path.getmtime are mocked
            # in tests to ensure deterministic age calculations.
            try:
                mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime)
                return (self.now - mtime).days > self.log_age_days
            except OSError:
                return False # File might have been deleted or inaccessible
        return False

    def _is_common_temp_file(self, path):
        if path.is_file():
            filename = path.name.lower()
            return (
                filename == '.ds_store' or
                filename == 'thumbs.db' or
                filename.endswith('.tmp') or
                path.parent.name == '__pycache__'
            )
        return False

    def find_dust_bunnies(self):
        self.dust_bunnies = []
        for root_path in self.root_paths:
            if not root_path.exists():
                print(f"Warning: Path not found: {root_path}")
                continue

            for dirpath_str, dirnames, filenames in os.walk(root_path):
                dirpath = Path(dirpath_str)

                # Check files
                for f in filenames:
                    file_path = dirpath / f
                    if self._is_common_temp_file(file_path) or self._is_old_log_file(file_path):
                        self.dust_bunnies.append(file_path)

                # Check empty directories (after processing files in them)
                # We need to iterate dirnames in reverse to catch empty subdirs first
                # This is handled by os.walk's natural bottom-up traversal for empty dirs
                # For empty dirs, we check after all files/subdirs are processed.
                # A directory is considered empty if it contains no files and no subdirectories
                # that are not themselves dust bunnies.
                # A simpler approach for os.walk is to check after the walk is complete.
                # For now, we'll collect empty dirs as we find them, but they might become non-empty
                # if we delete files from them. A second pass or a more complex logic is needed
                # for perfect empty dir cleanup. For simplicity, we'll check at the end.

        # Second pass for empty directories, after potential file deletions
        # This is a simplified approach. A more robust solution would require
        # iterating from deepest to shallowest directories.
        # For this utility, we'll just find currently empty directories.
        for root_path in self.root_paths:
            for dirpath_str, dirnames, filenames in os.walk(root_path):
                dirpath = Path(dirpath_str)
                if self._is_empty_dir(dirpath) and dirpath not in self.dust_bunnies:
                    # Ensure we don't add the root path itself if it becomes empty
                    if dirpath != root_path:
                        self.dust_bunnies.append(dirpath)

        return self.dust_bunnies

    def clean_dust_bunnies(self):
        if not self.dust_bunnies:
            print("No cosmic dust bunnies found to clean.")
            return

        print(f"{'[DRY RUN] ' if self.dry_run else ''}Identified {len(self.dust_bunnies)} cosmic dust bunnies:")
        for bunny in self.dust_bunnies:
            print(f"  - {bunny}")

        if self.dry_run:
            print("\nThis was a dry run. No files were deleted. Use --clean to perform actual deletion.")
            return

        print("\nInitiating cosmic cleanup...")
        deleted_count = 0
        for bunny in sorted(self.dust_bunnies, key=lambda p: len(p.parts), reverse=True): # Delete deeper paths first
            try:
                if bunny.is_file():
                    # Mock rationale: os.remove is mocked in tests to prevent actual file deletion.
                    os.remove(bunny)
                    print(f"  Deleted file: {bunny}")
                    deleted_count += 1
                elif bunny.is_dir():
                    # Mock rationale: os.rmdir is mocked in tests to prevent actual directory deletion.
                    # Ensure directory is truly empty before attempting rmdir
                    if not list(bunny.iterdir()):
                        os.rmdir(bunny)
                        print(f"  Deleted empty directory: {bunny}")
                        deleted_count += 1
                    else:
                        print(f"  Skipped non-empty directory: {bunny}")
            except OSError as e:
                print(f"  Error deleting {bunny}: {e}")
        print(f"\nCosmic cleanup complete. {deleted_count} items removed.")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Scans directories for temporary files, old logs, and empty folders."
    )
    parser.add_argument(
        'paths', metavar='PATH', type=str, nargs='+',
        help='One or more root directories to scan.'
    )
    parser.add_argument(
        '--clean', action='store_true',
        help='Perform actual deletion of identified items (default is dry run).'
    )
    parser.add_argument(
        '--log-age', type=int, default=7,
        help='Number of days after which .log files are considered old and can be deleted (default: 7).'
    )

    args = parser.parse_args()

    collector = CosmicDustBunnyCollector(args.paths, args.log_age, dry_run=not args.clean)
    collector.find_dust_bunnies()
    collector.clean_dust_bunnies()

if __name__ == '__main__':
    main()
