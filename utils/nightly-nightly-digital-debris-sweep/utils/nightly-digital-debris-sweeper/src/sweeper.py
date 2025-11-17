import os
import shutil
import fnmatch
import argparse
from datetime import datetime, timedelta

class DigitalDebrisSweeper:
    def __init__(self, patterns, quarantine_dir=None, age_days=0):
        self.patterns = patterns
        self.quarantine_dir = quarantine_dir
        self.age_days = age_days

    def _is_debris(self, filepath):
        filename = os.path.basename(filepath)
        for pattern in self.patterns:
            if fnmatch.fnmatch(filename, pattern):
                if self.age_days > 0:
                    # Check file age
                    modified_timestamp = os.path.getmtime(filepath)
                    modified_date = datetime.fromtimestamp(modified_timestamp)
                    if datetime.now() - modified_date > timedelta(days=self.age_days):
                        return True
                else:
                    return True
        return False

    def find_debris(self, scan_dirs):
        debris_files = []
        for scan_dir in scan_dirs:
            if not os.path.isdir(scan_dir):
                print(f"Warning: Scan directory '{scan_dir}' does not exist or is not a directory. Skipping.")
                continue
            for root, _, files in os.walk(scan_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self._is_debris(filepath):
                        debris_files.append(filepath)
        return debris_files

    def quarantine_debris(self, debris_files):
        if not self.quarantine_dir:
            raise ValueError("Quarantine directory must be specified for quarantining debris.")

        # Ensure quarantine directory exists
        os.makedirs(self.quarantine_dir, exist_ok=True)

        quarantined_count = 0
        for filepath in debris_files:
            try:
                dest_path = os.path.join(self.quarantine_dir, os.path.basename(filepath))
                # Handle potential name collisions in quarantine_dir
                counter = 1
                original_dest_path = dest_path
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(original_dest_path)
                    dest_path = f"{name}_{counter}{ext}"
                    counter += 1

                shutil.move(filepath, dest_path)
                print(f"Quarantined: '{filepath}' -> '{dest_path}'")
                quarantined_count += 1
            except Exception as e:
                print(f"Error quarantining '{filepath}': {e}")
        return quarantined_count

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Digital Debris Sweeper: Scans for and quarantines temporary/log files."
    )
    parser.add_argument(
        "scan_dirs",
        nargs=":",
        help="One or more directories to scan for debris."
    )
    parser.add_argument(
        "--patterns",
        nargs=":",
        default=["*.log", "*.tmp", "*~", "*.bak", "*.old"],
        help="File patterns to identify as debris (e.g., '*.log', '*.tmp'). Default: *.log *.tmp *~ *.bak *.old"
    )
    parser.add_argument(
        "--quarantine-dir",
        help="Directory to move identified debris files to. If not specified, files will only be listed."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=0,
        help="Only consider files older than this many days as debris. Set to 0 to ignore age. Default: 0"
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only list debris files, do not move them. Overrides --quarantine-dir if present."
    )

    args = parser.parse_args()

    if not args.scan_dirs:
        print("Error: At least one scan directory must be provided.")
        parser.print_help()
        exit(1)

    sweeper = DigitalDebrisSweeper(
        patterns=args.patterns,
        quarantine_dir=args.quarantine_dir,
        age_days=args.age_days
    )

    print(f"Scanning directories: {', '.join(args.scan_dirs)}")
    print(f"Looking for patterns: {', '.join(args.patterns)}")
    if args.age_days > 0:
        print(f"Considering files older than {args.age_days} days.")

    debris_found = sweeper.find_debris(args.scan_dirs)

    if not debris_found:
        print("No digital debris found. Your digital space is pristine... for now.")
        return

    print("\n--- Identified Digital Debris ---")
    for f in debris_found:
        print(f"- {f}")
    print(f"Total debris files found: {len(debris_found)}")

    if args.quarantine_dir and not args.list_only:
        print(f"\n--- Quarantining Debris to '{args.quarantine_dir}' ---")
        try:
            quarantined_count = sweeper.quarantine_debris(debris_found)
            print(f"Successfully quarantined {quarantined_count} files.")
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
    elif args.list_only:
        print("\n(List-only mode: no files were moved.)")
    else:
        print("\n(No quarantine directory specified. Files were only listed.)")

if __name__ == "__main__":
    main()
