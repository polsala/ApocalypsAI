import os
import time
import argparse
from datetime import datetime, timedelta

class DigitalDustBunnySweeper:
    def __init__(self, path_to_scan, log_age_days=30):
        self.path_to_scan = os.path.abspath(path_to_scan)
        self.log_age_seconds = log_age_days * 24 * 60 * 60
        self.current_time = time.time()
        self.temp_extensions = ('.tmp', '.bak', '~', '.swp', '.temp')

        self.empty_dirs = []
        self.old_log_files = []
        self.temp_files = []

    def _is_empty_dir(self, path):
        return not os.listdir(path)

    def _is_old_log_file(self, file_path):
        if file_path.lower().endswith(('.log', '.txt')):
            try:
                mtime = os.path.getmtime(file_path)
                return (self.current_time - mtime) > self.log_age_seconds
            except OSError:
                return False # File might be inaccessible
        return False

    def _is_temporary_file(self, file_path):
        return file_path.lower().endswith(self.temp_extensions) or \
               os.path.basename(file_path).startswith(('~', '#')) or \
               'temp' in os.path.basename(file_path).lower()

    def scan(self):
        if not os.path.isdir(self.path_to_scan):
            print(f"Error: Path '{self.path_to_scan}' is not a valid directory.")
            return

        print(f"Scanning {self.path_to_scan} for digital dust bunnies...")

        for root, dirs, files in os.walk(self.path_to_scan, topdown=False):
            # Check for empty directories (bottom-up approach)
            if not dirs and not files:
                self.empty_dirs.append(root)

            for file in files:
                file_path = os.path.join(root, file)
                if self._is_old_log_file(file_path):
                    self.old_log_files.append(file_path)
                if self._is_temporary_file(file_path):
                    self.temp_files.append(file_path)

    def report(self):
        print("\n--- Empty Directories Found ---")
        if self.empty_dirs:
            for d in self.empty_dirs:
                print(f"  - {d}")
        else:
            print("  No empty directories found.")

        print(f"\n--- Old Log Files Found (older than {self.log_age_seconds // (24*60*60)} days) ---")
        if self.old_log_files:
            for f in self.old_log_files:
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d')
                    print(f"  - {f} (last modified: {mtime})")
                except OSError:
                    print(f"  - {f} (inaccessible)")
        else:
            print("  No old log files found.")

        print("\n--- Temporary Files Found ---")
        if self.temp_files:
            for f in self.temp_files:
                print(f"  - {f}")
        else:
            print("  No temporary files found.")

    def delete_dust_bunnies(self):
        print("\n--- Deleting Dust Bunnies ---")
        deleted_count = 0

        for f in self.temp_files:
            try:
                os.remove(f)
                print(f"  Deleted temporary file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting {f}: {e}")

        for f in self.old_log_files:
            try:
                os.remove(f)
                print(f"  Deleted old log file: {f}")
                deleted_count += 1
            except OSError as e:
                print(f"  Error deleting {f}: {e}")

        # Delete empty directories, starting from deepest
        for d in sorted(self.empty_dirs, key=len, reverse=True):
            try:
                # Re-check if directory is still empty, as files might have been deleted from it
                if not os.listdir(d):
                    os.rmdir(d)
                    print(f"  Deleted empty directory: {d}")
                    deleted_count += 1
                else:
                    print(f"  Skipped non-empty directory: {d}")
            except OSError as e:
                print(f"  Error deleting {d}: {e}")

        print(f"\nTotal {deleted_count} dust bunnies swept away!")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away digital dust bunnies (empty dirs, old logs, temp files)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to scan for digital dust bunnies."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Actually delete the identified files and directories. Use with caution!"
    )
    parser.add_argument(
        "--log-age",
        type=int,
        default=30,
        help="Number of days after which a log file is considered 'old'. Default is 30."
    )

    args = parser.parse_args()

    sweeper = DigitalDustBunnySweeper(args.path, args.log_age)
    sweeper.scan()
    sweeper.report()

    if args.delete:
        confirm = input("Are you sure you want to delete these files and directories? (yes/no): ")
        if confirm.lower() == 'yes':
            sweeper.delete_dust_bunnies()
        else:
            print("Deletion cancelled.")
    else:
        print("\nDry run complete. No files or directories were deleted.")
        print("Run with --delete to remove these dust bunnies.")

if __name__ == "__main__":
    main()
