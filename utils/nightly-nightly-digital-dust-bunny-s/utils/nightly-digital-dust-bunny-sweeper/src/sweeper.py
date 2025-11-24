import os
import argparse
import fnmatch
import sys

class DigitalDustBunnySweeper:
    """
    A utility to identify and optionally clean up old, unused, or temporary files
    and empty directories within a project.
    """
    def __init__(self, root_path, patterns, empty_dirs, exclude_paths, dry_run):
        self.root_path = os.path.abspath(root_path)
        self.patterns = patterns
        self.empty_dirs = empty_dirs
        self.exclude_paths = [os.path.abspath(p) for p in exclude_paths]
        self.dry_run = dry_run
        self.found_items = []

        if not os.path.isdir(self.root_path):
            raise ValueError(f"Error: Root path '{self.root_path}' is not a valid directory.")

    def _is_excluded(self, path):
        """Checks if a given path is explicitly excluded."""
        abs_path = os.path.abspath(path)
        for excluded in self.exclude_paths:
            if abs_path == excluded or abs_path.startswith(excluded + os.sep):
                return True
        return False

    def _find_dust_bunnies(self):
        """Scans the directory tree for files matching patterns and empty directories."""
        print(f"Scanning '{self.root_path}' for digital dust bunnies...")
        for dirpath, dirnames, filenames in os.walk(self.root_path, topdown=False):
            if self._is_excluded(dirpath):
                dirnames[:] = [] # Don't recurse into excluded directories
                continue

            # Check files
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if self._is_excluded(file_path):
                    continue
                for pattern in self.patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        self.found_items.append(('file', file_path))
                        break # Found a match, move to next file

            # Check for empty directories (after processing files and subdirectories)
            if self.empty_dirs and not os.listdir(dirpath): # os.listdir is empty if no files/dirs
                if dirpath != self.root_path: # Don't remove the root path itself if it becomes empty
                    self.found_items.append(('dir', dirpath))

    def _report_dust_bunnies(self):
        """Prints a report of identified items."""
        if not self.found_items:
            print("\n✨ No digital dust bunnies found! Your repository is sparkling clean.")
            return

        print(f"\n--- Digital Dust Bunny Report ({'DRY RUN' if self.dry_run else 'CLEANUP'}) ---")
        for item_type, item_path in self.found_items:
            action = "Would delete" if self.dry_run else "Deleting"
            print(f"  [{item_type.upper()}] {action}: {item_path}")
        print(f"--------------------------------------------------")
        print(f"Total items identified: {len(self.found_items)}")

    def _clean_dust_bunnies(self):
        """Deletes identified files and empty directories."""
        if self.dry_run:
            return

        for item_type, item_path in self.found_items:
            try:
                if item_type == 'file':
                    os.remove(item_path)
                elif item_type == 'dir':
                    os.rmdir(item_path)
                print(f"  ✅ Deleted {item_type}: {item_path}")
            except OSError as e:
                print(f"  ❌ Failed to delete {item_type} '{item_path}': {e}")

    def sweep(self):
        """Executes the sweeping process."""
        self._find_dust_bunnies()
        self._report_dust_bunnies()
        self._clean_dust_bunnies()
        if not self.dry_run and self.found_items:
            print("\nCleanup complete. May your repository remain pristine!")
        elif not self.found_items:
            print("\nNo cleanup needed.")

def main():
    parser = argparse.ArgumentParser(
        description="Identify and optionally clean up old, unused, or temporary files and empty directories."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=['*.log', '*.tmp', '__pycache__', '.DS_Store', 'Thumbs.db'],
        help="Space-separated list of glob patterns for files to identify (e.g., '*.log', '__pycache__')."
    )
    parser.add_argument(
        "--empty-dirs",
        action="store_true",
        help="Include empty directories in the cleanup scan."
    )
    parser.add_argument(
        "--exclude",
        nargs='*',
        default=[],
        help="Space-separated list of paths (files or directories) to explicitly exclude from scanning."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="DANGER! Execute the cleanup, deleting identified files and empty directories. Use with caution."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="(Default) Only report what *would* be cleaned, without making any changes. Overridden by --clean."
    )

    args = parser.parse_args()

    # If --clean is provided, it overrides --dry-run
    dry_run = not args.clean

    try:
        sweeper = DigitalDustBunnySweeper(
            root_path=args.path,
            patterns=args.patterns,
            empty_dirs=args.empty_dirs,
            exclude_paths=args.exclude,
            dry_run=dry_run
        )
        sweeper.sweep()
        sys.exit(0)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
