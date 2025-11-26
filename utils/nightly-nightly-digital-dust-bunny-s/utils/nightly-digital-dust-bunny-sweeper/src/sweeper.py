import os
import shutil
from pathlib import Path
import argparse

class DigitalDustBunnySweeper:
    def __init__(self, root_dir: Path, dry_run: bool = False):
        self.root_dir = root_dir.resolve()
        self.dry_run = dry_run
        self.patterns = [
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "build",
            "dist",
            "node_modules",
            "target", # For Rust projects, though less common in Python repos
        ]
        self.found_items = []

    def _find_items(self):
        print(f"Scanning '{self.root_dir}' for digital dust bunnies...")
        for root, dirs, files in os.walk(self.root_dir):
            # Avoid scanning inside found items to prevent redundant work or errors
            # if a parent directory is already marked for deletion.
            # Create a copy of dirs to modify it during iteration
            dirs_to_process = list(dirs)
            dirs[:] = [d for d in dirs_to_process if d not in self.patterns]

            current_path = Path(root)
            for pattern in self.patterns:
                item_path = current_path / pattern
                if item_path.exists(): # Check if the path actually exists on disk
                    if item_path.is_dir() or item_path.is_file(): # Ensure it's a file or directory
                        self.found_items.append(item_path)
                        print(f"  Found: {item_path}")
        if not self.found_items:
            print("No digital dust bunnies found. Your repository is sparkling clean!")

    def sweep(self):
        self._find_items()
        if not self.found_items:
            return

        print("\n--- Sweeping Summary ---")
        if self.dry_run:
            print("DRY RUN: No files will be deleted.")
        else:
            print("DELETING files...")

        for item_path in self.found_items:
            try:
                if item_path.is_dir():
                    if not self.dry_run:
                        shutil.rmtree(item_path)
                    print(f"  {'Would delete' if self.dry_run else 'Deleted'} directory: {item_path}")
                elif item_path.is_file():
                    if not self.dry_run:
                        os.remove(item_path)
                    print(f"  {'Would delete' if self.dry_run else 'Deleted'} file: {item_path}")
            except OSError as e:
                print(f"  Error {'deleting' if not self.dry_run else 'accessing'}: {item_path} - {e}")

        print("\nSweeping complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Sweep away common build caches and temporary files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without actually deleting any files.",
    )
    args = parser.parse_args()

    sweeper = DigitalDustBunnySweeper(Path(args.path), args.dry_run)
    sweeper.sweep()

if __name__ == "__main__":
    main()
