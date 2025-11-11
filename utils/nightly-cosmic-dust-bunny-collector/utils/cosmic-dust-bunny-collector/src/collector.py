import os
import datetime
import argparse
import shutil

class CosmicDustBunnyCollector:
    def __init__(self, target_dir, age_days, dry_run=True, recursive=False, quarantine_dir=None):
        if not os.path.isdir(target_dir):
            raise ValueError(f"Target directory '{target_dir}' does not exist.")
        self.target_dir = os.path.abspath(target_dir)
        self.age_threshold = datetime.timedelta(days=age_days)
        self.dry_run = dry_run
        self.recursive = recursive
        self.quarantine_dir = quarantine_dir
        if self.quarantine_dir and not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)

    def _is_dust_bunny(self, filepath):
        """Checks if a file is older than the age threshold."""
        try:
            mod_time_timestamp = os.path.getmtime(filepath)
            mod_time = datetime.datetime.fromtimestamp(mod_time_timestamp)
            return datetime.datetime.now() - mod_time > self.age_threshold
        except OSError:
            # File might have been deleted between os.walk and os.path.getmtime
            return False

    def find_dust_bunnies(self):
        """Finds all 'cosmic dust bunnies' (old files) in the target directory."""
        dust_bunnies = []
        if self.recursive:
            for root, _, files in os.walk(self.target_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self._is_dust_bunny(filepath):
                        dust_bunnies.append(filepath)
        else:
            for item in os.listdir(self.target_dir):
                filepath = os.path.join(self.target_dir, item)
                if os.path.isfile(filepath) and self._is_dust_bunny(filepath):
                    dust_bunnies.append(filepath)
        return dust_bunnies

    def collect_dust_bunnies(self):
        """Processes the found dust bunnies based on dry_run and quarantine_dir settings."""
        found_bunnies = self.find_dust_bunnies()
        if not found_bunnies:
            print("No cosmic dust bunnies found. Your digital space is pristine... for now.")
            return []

        print(f"Detected {len(found_bunnies)} cosmic dust bunnies older than {self.age_threshold.days} days:")
        for bunny in found_bunnies:
            print(f"  - {bunny}")

        if self.dry_run:
            print("\n(Dry run: No files will be moved or deleted.)")
            return found_bunnies
        
        processed_bunnies = []
        for bunny in found_bunnies:
            try:
                if self.quarantine_dir:
                    dest_path = os.path.join(self.quarantine_dir, os.path.basename(bunny))
                    # Handle potential name collisions in quarantine
                    counter = 1
                    original_dest_path = dest_path
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(os.path.basename(original_dest_path))
                        dest_path = os.path.join(self.quarantine_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.move(bunny, dest_path)
                    print(f"  Moved '{bunny}' to quarantine: '{dest_path}'")
                else:
                    os.remove(bunny)
                    print(f"  Removed '{bunny}'")
                processed_bunnies.append(bunny)
            except OSError as e:
                print(f"  Error processing '{bunny}': {e}")
        
        print("\nCosmic dust bunny collection complete!")
        return processed_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Identify and optionally remove old, unused files."
    )
    parser.add_argument(
        "target_directory",
        help="The directory to scan for cosmic dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="Files older than this many days will be considered dust bunnies. (Default: 90)"
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_true",
        help="Perform actual file operations (move/delete). By default, it's a dry run."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively."
    )
    parser.add_argument(
        "--quarantine",
        type=str,
        help="Move identified files to this directory instead of deleting them. Creates the directory if it doesn't exist."
    )

    args = parser.parse_args()

    try:
        collector = CosmicDustBunnyCollector(
            target_dir=args.target_directory,
            age_days=args.age,
            dry_run=not args.no_dry_run,
            recursive=args.recursive,
            quarantine_dir=args.quarantine
        )
        collector.collect_dust_bunnies()
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
