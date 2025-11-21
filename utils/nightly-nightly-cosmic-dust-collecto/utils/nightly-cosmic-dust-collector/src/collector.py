import os
import shutil
import hashlib
import json
import argparse
from datetime import datetime

class CosmicDustCollector:
    def __init__(self, source_dir, dustbin_dir):
        self.source_dir = os.path.abspath(source_dir)
        self.dustbin_dir = os.path.abspath(dustbin_dir)
        self.manifest_path = os.path.join(self.dustbin_dir, '_dust_manifest.json')
        self.manifest = {}

        os.makedirs(self.dustbin_dir, exist_ok=True)
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")

        self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                try:
                    self.manifest = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode manifest at {self.manifest_path}. Starting fresh.")
                    self.manifest = {}

    def _save_manifest(self):
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=4)

    def _calculate_file_hash(self, filepath, block_size=65536):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()

    def collect_dust(self):
        print(f"Scanning source directory: {self.source_dir}")
        current_files = set()

        for root, _, files in os.walk(self.source_dir):
            for filename in files:
                source_filepath = os.path.join(root, filename)
                # Relative path from source_dir to handle subdirectories
                relative_filepath = os.path.relpath(source_filepath, self.source_dir)
                current_files.add(relative_filepath)

                try:
                    current_hash = self._calculate_file_hash(source_filepath)
                    current_mtime = os.path.getmtime(source_filepath)
                except IOError as e:
                    print(f"Error reading file {source_filepath}: {e}. Skipping.")
                    continue

                manifest_entry = self.manifest.get(relative_filepath)

                if not manifest_entry or \
                   manifest_entry['hash'] != current_hash or \
                   manifest_entry['mtime'] != current_mtime:
                    
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Preserve directory structure in dustbin
                    dustbin_subdir = os.path.join(self.dustbin_dir, os.path.dirname(relative_filepath))
                    os.makedirs(dustbin_subdir, exist_ok=True)
                    
                    dustbin_filename = f"{os.path.basename(relative_filepath)}.{timestamp}.bak"
                    dustbin_filepath = os.path.join(dustbin_subdir, dustbin_filename)

                    print(f"Archiving changed file: {relative_filepath} to {dustbin_filepath}")
                    try:
                        shutil.copy2(source_filepath, dustbin_filepath)
                        self.manifest[relative_filepath] = {
                            'hash': current_hash,
                            'mtime': current_mtime,
                            'last_archived': timestamp
                        }
                    except IOError as e:
                        print(f"Error archiving {source_filepath}: {e}. Skipping.")

        # Remove entries for files that no longer exist in the source directory
        files_to_remove_from_manifest = [f for f in self.manifest if f not in current_files]
        for f in files_to_remove_from_manifest:
            print(f"File no longer exists: {f}. Removing from manifest.")
            del self.manifest[f]

        self._save_manifest()
        print("Cosmic dust collection complete.")

def main():
    parser = argparse.ArgumentParser(
        description="Collects 'cosmic dust' by archiving changed files."
    )
    parser.add_argument('--source', required=True, help='The directory to monitor for file changes.')
    parser.add_argument('--dustbin', required=True, help='The directory where archived file versions will be stored.')

    args = parser.parse_args()

    try:
        collector = CosmicDustCollector(args.source, args.dustbin)
        collector.collect_dust()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
