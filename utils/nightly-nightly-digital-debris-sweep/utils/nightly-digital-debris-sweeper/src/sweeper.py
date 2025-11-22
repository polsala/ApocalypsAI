import os
import shutil
import argparse
from datetime import datetime, timedelta

class DigitalDebrisSweeper:
    COMMON_DEBRIS_PATTERNS = [
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        "target",  # Rust
        "dist",    # Python/JS build artifacts
        "build",   # C/C++/Java build artifacts
        ".mypy_cache",
        ".venv",   # Python virtual environments
        "venv",
    ]

    def __init__(self, root_dir: str, age_threshold_days: int = 30):
        if not os.path.isdir(root_dir):
            raise ValueError(f"Root directory '{root_dir}' does not exist or is not a directory.")
        self.root_dir = os.path.abspath(root_dir)
        self.age_threshold = timedelta(days=age_threshold_days)
        self.current_time = datetime.now()

    def _is_debris_dir(self, dir_name: str) -> bool:
        """Checks if a directory name matches a known debris pattern."""
        return dir_name in self.COMMON_DEBRIS_PATTERNS

    def _is_old(self, path: str) -> bool:
        """Checks if a path's last modification time is older than the threshold."""
        try:
            mtime_timestamp = os.path.getmtime(path)
            mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
            return (self.current_time - mtime_datetime) > self.age_threshold
        except OSError:
            # Handle cases where file might be deleted between walk and getmtime
            return False

    def find_debris(self) -> list[str]:
        """Finds and returns a list of old debris directories."""
        debris_candidates = []
        for root, dirs, _ in os.walk(self.root_dir):
            # Make a copy of dirs to modify it during iteration
            dirs_copy = list(dirs)
            for dir_name in dirs_copy:
                if self._is_debris_dir(dir_name):
                    full_path = os.path.join(root, dir_name)
                    if os.path.isdir(full_path) and self._is_old(full_path):
                        debris_candidates.append(full_path)
                        # Don't descend into known debris directories
                        try:
                            dirs.remove(dir_name)
                        except ValueError:
                            pass # Already removed or not in current dirs list
        return debris_candidates

    def clean_debris(self, debris_paths: list[str]) -> list[str]:
        """Deletes the specified debris directories."""
        deleted_paths = []
        for path in debris_paths:
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    deleted_paths.append(path)
                    print(f"Deleted: {path}")
                except OSError as e:
                    print(f"Error deleting {path}: {e}")
            else:
                print(f"Warning: Path '{path}' no longer exists or is not a directory. Skipping.")
        return deleted_paths

def main():
    parser = argparse.ArgumentParser(
        description="Sweeps away old digital debris (cache/build directories) from a specified path."
    )
    parser.add_argument(
        "root_directory",
        type=str,
        help="The root directory to start sweeping from."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Age threshold in days. Debris older than this will be considered for deletion. (default: 30)"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Perform actual deletion of identified debris. If not set, only lists candidates."
    )

    args = parser.parse_args()

    try:
        sweeper = DigitalDebrisSweeper(args.root_directory, args.age)
        print(f"Scanning '{sweeper.root_dir}' for debris older than {args.age} days...")
        debris_to_clean = sweeper.find_debris()

        if not debris_to_clean:
            print("No old digital debris found. Your digital space is pristine!")
            return

        print("\n--- Identified Digital Debris ---")
        for path in debris_to_clean:
            print(f"- {path}")
        print("---------------------------------\n")

        if args.delete:
            print("Initiating debris removal...")
            deleted_count = len(sweeper.clean_debris(debris_to_clean))
            print(f"\nSuccessfully removed {deleted_count} debris directories.")
        else:
            print(f"Found {len(debris_to_clean)} debris directories. Use --delete to remove them.")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
