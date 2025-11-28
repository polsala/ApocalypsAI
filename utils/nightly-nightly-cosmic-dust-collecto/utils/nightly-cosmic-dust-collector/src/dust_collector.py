import os
import shutil
import argparse
import datetime
import time

class CosmicDustCollector:
    def __init__(self, root_dir, max_size_bytes=1024, max_age_days=90, empty_only=False):
        self.root_dir = os.path.abspath(root_dir)
        self.max_size_bytes = max_size_bytes
        self.max_age_days = max_age_days
        self.empty_only = empty_only
        self.archive_dir = os.path.join(self.root_dir, '.cosmic_dust_archive')

    def _is_dust(self, filepath):
        try:
            stat = os.stat(filepath)
            file_size = stat.st_size
            file_mtime = stat.st_mtime

            is_empty = file_size == 0
            is_small = file_size < self.max_size_bytes
            is_old = (time.time() - file_mtime) > (self.max_age_days * 24 * 60 * 60)

            if self.empty_only:
                return is_empty
            else:
                return is_empty or (is_small and is_old)
        except OSError:
            return False # File might have been deleted or inaccessible

    def find_dust(self):
        dust_files = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Exclude the archive directory itself from being scanned
            if os.path.abspath(dirpath).startswith(self.archive_dir):
                continue
            # Prevent os.walk from descending into the archive directory
            if '.cosmic_dust_archive' in dirnames:
                dirnames.remove('.cosmic_dust_archive')

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if self._is_dust(filepath):
                    dust_files.append(filepath)
        return dust_files

    def list_dust(self):
        dust_files = self.find_dust()
        if not dust_files:
            print("No cosmic dust found. Your repository is sparkling clean!")
            return 0

        print(f"Found {len(dust_files)} cosmic dust files:")
        for f in dust_files:
            print(f"  - {f}")
        return len(dust_files)

    def archive_dust(self):
        dust_files = self.find_dust()
        if not dust_files:
            print("No cosmic dust found to archive.")
            return 0

        os.makedirs(self.archive_dir, exist_ok=True)
        archived_count = 0
        for f in dust_files:
            try:
                # Preserve directory structure within the archive
                relative_path = os.path.relpath(f, self.root_dir)
                archive_filepath = os.path.join(self.archive_dir, relative_path)
                os.makedirs(os.path.dirname(archive_filepath), exist_ok=True)
                shutil.move(f, archive_filepath)
                print(f"Archived: {f} -> {archive_filepath}")
                archived_count += 1
            except OSError as e:
                print(f"Error archiving {f}: {e}")
        print(f"Successfully archived {archived_count} cosmic dust files to {self.archive_dir}")
        return archived_count

    def delete_dust(self):
        dust_files = self.find_dust()
        if not dust_files:
            print("No cosmic dust found to delete.")
            return 0

        deleted_count = 0
        for f in dust_files:
            try:
                os.remove(f)
                print(f"Deleted: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting {f}: {e}")
        print(f"Successfully deleted {deleted_count} cosmic dust files.")
        return deleted_count

def main():
    parser = argparse.ArgumentParser(description="Nightly Cosmic Dust Collector: Clean up small, old, or empty files.")
    parser.add_argument("action", choices=["list", "archive", "delete"], help="Action to perform: list, archive, or delete dust files.")
    parser.add_argument("path", default=".", nargs="?", help="Root directory to scan for dust. Defaults to current directory.")
    parser.add_argument("--max-size", type=int, default=1024, help="Maximum file size in bytes to consider as 'small' dust (default: 1024 bytes).")
    parser.add_argument("--max-age", type=int, default=90, help="Maximum file age in days to consider as 'old' dust (default: 90 days).")
    parser.add_argument("--empty-only", action="store_true", help="Only consider empty files as dust, ignoring size/age criteria.")

    args = parser.parse_args()

    collector = CosmicDustCollector(
        root_dir=args.path,
        max_size_bytes=args.max_size,
        max_age_days=args.max_age,
        empty_only=args.empty_only
    )

    if args.action == "list":
        collector.list_dust()
    elif args.action == "archive":
        collector.archive_dust()
    elif args.action == "delete":
        collector.delete_dust()

if __name__ == "__main__":
    main()
