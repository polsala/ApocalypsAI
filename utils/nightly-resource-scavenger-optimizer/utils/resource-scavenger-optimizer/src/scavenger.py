import os
import hashlib
import argparse
from collections import defaultdict

class ResourceScavenger:
    def __init__(self, path, min_size_mb=10):
        if not os.path.isdir(path):
            raise ValueError(f"Path '{path}' is not a valid directory.")
        self.path = os.path.abspath(path)
        self.min_size_bytes = min_size_mb * 1024 * 1024
        self.large_files = []
        self.duplicate_files = defaultdict(list)

    def _get_file_hash(self, filepath, block_size=65536):
        # Mock rationale: In a real scenario, reading large files can be slow.
        # For testing, we might mock this to return a predictable hash for a given file content.
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()

    def scan_for_large_files(self):
        print(f"[INFO] Scanning for files larger than {self.min_size_bytes / (1024*1024):.1f} MB...")
        for root, _, files in os.walk(self.path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    if size >= self.min_size_bytes:
                        self.large_files.append((filepath, size))
                except OSError as e:
                    print(f"[WARNING] Could not access '{filepath}': {e}")
        self.large_files.sort(key=lambda x: x[1], reverse=True)

    def find_duplicate_files(self):
        print("[INFO] Searching for duplicate files...")
        files_by_size = defaultdict(list)
        for root, _, files in os.walk(self.path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    files_by_size[size].append(filepath)
                except OSError as e:
                    print(f"[WARNING] Could not access '{filepath}': {e}")

        for size, filepaths in files_by_size.items():
            if size == 0 or len(filepaths) < 2: # Skip empty files and unique files
                continue
            
            hashes = defaultdict(list)
            for filepath in filepaths:
                file_hash = self._get_file_hash(filepath)
                hashes[file_hash].append(filepath)
            
            for file_hash, paths in hashes.items():
                if len(paths) > 1:
                    self.duplicate_files[file_hash].extend(paths)

    def generate_report(self):
        report = []
        report.append("--- Resource Scavenger Report ---")
        report.append(f"Scanning: {self.path}")
        report.append("")

        if self.large_files:
            report.append(f"[LARGE FILES ( > {self.min_size_bytes / (1024*1024):.1f} MB )]")
            for filepath, size in self.large_files:
                report.append(f"  - {filepath} ({size / (1024*1024):.1f} MB)")
            report.append("")
        else:
            report.append(f"[LARGE FILES ( > {self.min_size_bytes / (1024*1024):.1f} MB )]")
            report.append("  No excessively large files detected. Good job, scavenger!")
            report.append("")

        if self.duplicate_files:
            report.append("[DUPLICATE FILES]")
            for file_hash, paths in self.duplicate_files.items():
                report.append(f"  - Hash: {file_hash}")
                for p in paths:
                    report.append(f"    - {p}")
            report.append("")
        else:
            report.append("[DUPLICATE FILES]")
            report.append("  No duplicate files found. Your data is uniquely precious!")
            report.append("")

        report.append("--- Scavenging complete! ---")
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Scavenge for large and duplicate files to reclaim disk space."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The directory to scan."
    )
    parser.add_argument(
        "--min-size", 
        type=int, 
        default=10, 
        help="Minimum size in megabytes for a file to be considered 'large'. (Default: 10MB)"
    )
    parser.add_argument(
        "--duplicates", 
        action="store_true", 
        help="Flag to enable duplicate file detection."
    )

    args = parser.parse_args()

    try:
        scavenger = ResourceScavenger(args.path, args.min_size)
        if args.min_size > 0:
            scavenger.scan_for_large_files()
        if args.duplicates:
            scavenger.find_duplicate_files()
        print(scavenger.generate_report())
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
