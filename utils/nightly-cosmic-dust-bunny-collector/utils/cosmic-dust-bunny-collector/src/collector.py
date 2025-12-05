import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

class CosmicDustCollector:
    def __init__(self):
        self.temp_file_patterns = [
            '.tmp', '.bak', '.old', '.swp', '.swo', '.swn',
            '~', '#', '.DS_Store', 'Thumbs.db'
        ]
        self.findings: Dict[str, List[str]] = {
            'temp_files': [],
            'old_logs': [],
            'empty_dirs': []
        }

    def _is_temp_file(self, filepath: str) -> bool:
        filename = os.path.basename(filepath).lower()
        for pattern in self.temp_file_patterns:
            if pattern in filename or filename.startswith('.~') or filename.startswith('#') or filename.endswith('~'):
                return True
        return False

    def _is_old_log(self, filepath: str, age_days: int) -> bool:
        if not filepath.lower().endswith('.log'):
            return False
        try:
            mtime = os.path.getmtime(filepath)
            file_age_seconds = time.time() - mtime
            return file_age_seconds > (age_days * 24 * 3600)
        except OSError:
            return False

    def _is_empty_dir(self, dirpath: str) -> bool:
        if not os.path.isdir(dirpath):
            return False
        try:
            # Check if the directory is truly empty (no files or subdirectories)
            return not os.listdir(dirpath)
        except OSError:
            return False

    def scan(self, paths: List[str], age_days: int = 30) -> Dict[str, List[str]]:
        self.findings = {
            'temp_files': [],
            'old_logs': [],
            'empty_dirs': []
        }

        for path in paths:
            if not os.path.exists(path):
                print(f"Warning: Path not found - {path}", file=sys.stderr)
                continue

            # os.walk(topdown=False) ensures we process subdirectories before their parents.
            # This is crucial for correctly identifying empty directories after their contents
            # (which might be other empty directories or files) have been considered for deletion.
            for root, dirs, files in os.walk(path, topdown=False):
                # Check files
                for file in files:
                    filepath = os.path.join(root, file)
                    if self._is_temp_file(filepath):
                        self.findings['temp_files'].append(filepath)
                    elif self._is_old_log(filepath, age_days):
                        self.findings['old_logs'].append(filepath)

                # Check directories (after files in them are potentially removed/considered)
                if self._is_empty_dir(root):
                    self.findings['empty_dirs'].append(root)
        return self.findings

    def clean(self, findings: Dict[str, List[str]], dry_run: bool = True) -> Tuple[int, int]:
        deleted_files_count = 0
        deleted_dirs_count = 0

        if dry_run:
            print("--- DRY RUN MODE ---")
            print("The following items WOULD BE deleted:")
        else:
            print("--- CLEANING MODE ---")
            print("Deleting the following items:")

        has_findings = any(items for items in findings.values())

        if not has_findings:
            print("\nNo cosmic dust bunnies found. Your system is pristine!")
            return 0, 0

        for category, items in findings.items():
            if items:
                print(f"\n{category.replace('_', ' ').title()}:")
                for item in items:
                    print(f"  - {item}")
                    if not dry_run:
                        try:
                            if category in ['temp_files', 'old_logs']:
                                os.remove(item)
                                deleted_files_count += 1
                            elif category == 'empty_dirs':
                                os.rmdir(item)
                                deleted_dirs_count += 1
                            print(f"    [DELETED]")
                        except OSError as e:
                            print(f"    [ERROR] Could not delete {item}: {e}", file=sys.stderr)

        if dry_run:
            print("\nNo changes were made. Run without --dry-run to perform actual deletion.")
        else:
            print(f"\nCleanup complete. Deleted {deleted_files_count} files and {deleted_dirs_count} directories.")

        return deleted_files_count, deleted_dirs_count

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Scans and cleans up temporary files, old logs, and empty directories."
    )
    parser.add_argument(
        'command', choices=['scan', 'clean'],
        help="'scan' to list findings (dry run by default), 'clean' to perform actual deletion."
    )
    parser.add_argument(
        'paths', nargs='+',
        help="One or more paths to scan."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="Perform a dry run (list findings without deleting). This is the default for 'scan' command."
    )
    parser.add_argument(
        '--age-days', type=int, default=30,
        help="Age in days for log files to be considered 'old'. Default is 30 days."
    )

    args = parser.parse_args()

    collector = CosmicDustCollector()

    if args.command == 'scan':
        print(f"Scanning paths: {', '.join(args.paths)}")
        findings = collector.scan(args.paths, args.age_days)
        collector.clean(findings, dry_run=True) # 'scan' command is always a dry run
    elif args.command == 'clean':
        if args.dry_run:
            print("Warning: 'clean' command with --dry-run will only list. Remove --dry-run for actual deletion.")
        print(f"Scanning paths for cleanup: {', '.join(args.paths)}")
        findings = collector.scan(args.paths, args.age_days)
        collector.clean(findings, dry_run=not args.dry_run if args.command == 'clean' else True)

if __name__ == '__main__':
    main()
