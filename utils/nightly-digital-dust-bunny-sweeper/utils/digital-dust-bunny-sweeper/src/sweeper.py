import os
import time
import argparse
from datetime import datetime, timedelta

class DustBunny:
    def __init__(self, type, path, rationale, last_modified=None):
        self.type = type
        self.path = path
        self.rationale = rationale
        self.last_modified = last_modified

    def __str__(self):
        mod_str = f"\n  Last Modified: {self.last_modified.strftime('%Y-%m-%d %H:%M:%S')}" if self.last_modified else ""
        return f"[{self.type.upper()}]\n  Path: {self.path}{mod_str}\n  Rationale: {self.rationale}"

def find_dust_bunnies(root_path, age_days=30, current_time=None):
    """
    Scans the given root_path for digital 'dust bunnies' (empty directories, old logs, temp files).
    Args:
        root_path (str): The path to start scanning from.
        age_days (int): Number of days after which a log file is considered 'old'.
        current_time (datetime): The current time to use for age calculations. Defaults to now.
    Returns:
        list[DustBunny]: A list of identified dust bunnies.
    """
    if not os.path.isdir(root_path):
        # print(f"Error: Path '{root_path}' is not a valid directory.") # Suppress print in function for cleaner test output
        return []

    dust_bunnies = []
    temp_file_extensions = ('.tmp', '.bak', '.swp')
    temp_file_names = ('__pycache__', '.DS_Store')
    
    # Use provided current_time for deterministic testing, otherwise use actual now
    effective_current_time = current_time or datetime.now()
    min_mtime_for_old_logs = effective_current_time - timedelta(days=age_days)

    # Track all directories to check for emptiness later
    all_dirs = set()
    non_empty_dirs = set()

    for dirpath, dirnames, filenames in os.walk(root_path):
        all_dirs.add(dirpath)

        # Identify temporary files and old logs
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Common temporary/cache files
            if filename in temp_file_names or filename.endswith(temp_file_extensions):
                dust_bunnies.append(DustBunny(
                    type='temporary file',
                    path=file_path,
                    rationale=f"A transient file, likely left behind by a hurried process. Safe to sweep away."
                ))
                # Mark parent as non-empty due to this file
                non_empty_dirs.add(dirpath)

            # Old log files
            elif filename.endswith('.log'):
                try:
                    mtime_timestamp = os.path.getmtime(file_path)
                    mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                    if mtime_datetime < min_mtime_for_old_logs:
                        dust_bunnies.append(DustBunny(
                            type='old log file',
                            path=file_path,
                            rationale=f"This log file hasn't seen activity in {(effective_current_time - mtime_datetime).days} days. Perhaps it's time to archive or delete?",
                            last_modified=mtime_datetime
                        ))
                        # Mark parent as non-empty due to this file
                        non_empty_dirs.add(dirpath)
                except OSError:
                    # File might have been deleted between os.walk and os.path.getmtime
                    pass

        # Mark parent directories of any subdirectories or files as non-empty
        if dirnames or filenames:
            non_empty_dirs.add(dirpath)

    # Identify empty directories (recursively empty)
    # A directory is truly empty if it's in all_dirs but not in non_empty_dirs
    for d in all_dirs:
        if d not in non_empty_dirs:
            dust_bunnies.append(DustBunny(
                type='empty directory',
                path=d,
                rationale="This directory is utterly devoid of digital life. A prime candidate for removal."
            ))

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for 'digital dust bunnies' (empty folders, old logs, temporary files) and suggest cleanup actions."
    )
    parser.add_argument('--path', type=str, required=True, help='The root directory to start scanning from.')
    parser.add_argument('--age-days', type=int, default=30, help='Number of days after which a log file is considered \'old\'. Defaults to 30.')

    args = parser.parse_args()

    print(f"🧹 Initiating Digital Dust Bunny Sweep in {args.path}...")

    bunnies = find_dust_bunnies(args.path, args.age_days)

    if bunnies:
        print(f"\nFound {len(bunnies)} Digital Dust Bunnies:\n")
        for bunny in bunnies:
            print(bunny)
            print()
    else:
        print("\n✨ No digital dust bunnies found! Your digital realm is pristine.")

    print("\n✨ Sweep complete! Consider tidying these up to keep your digital realm pristine.")

if __name__ == '__main__':
    main()
