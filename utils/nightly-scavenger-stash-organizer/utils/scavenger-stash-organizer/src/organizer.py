import os
import shutil
import hashlib
import argparse
from collections import defaultdict

# Define file categories and their extensions
CATEGORIES = {
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.md'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
    'videos': ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'executables': ['.exe', '.dmg', '.app', '.sh', '.bat'] # Be cautious when automatically moving executables!
}

def get_file_category(filename):
    """Determines the category of a file based on its extension."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return 'others'

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def organize_stash(source_dir, dest_dir):
    """Organizes files from source_dir into categorized subdirectories in dest_dir."""
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    os.makedirs(dest_dir, exist_ok=True)
    print(f"\nOrganizing files from '{source_dir}' into '{dest_dir}'...")

    moved_count = 0
    # Convert paths to absolute to prevent issues with relative paths and subdirectories
    abs_source_dir = os.path.abspath(source_dir)
    abs_dest_dir = os.path.abspath(dest_dir)

    for root, _, files in os.walk(source_dir):
        for filename in files:
            source_filepath = os.path.join(root, filename)
            abs_source_filepath = os.path.abspath(source_filepath)

            # Skip if the file is already within the destination directory
            if abs_source_filepath.startswith(abs_dest_dir):
                print(f"  Skipped '{filename}' (already in destination or subfolder)")
                continue

            category = get_file_category(filename)
            
            category_dir = os.path.join(dest_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            
            destination_filepath = os.path.join(category_dir, filename)
            
            try:
                shutil.move(source_filepath, destination_filepath)
                print(f"  Moved '{filename}' to '{category_dir}'")
                moved_count += 1
            except shutil.Error as e:
                print(f"  Error moving '{filename}': {e}")
            except Exception as e:
                print(f"  An unexpected error occurred with '{filename}': {e}")

    print(f"\nOrganization complete. {moved_count} files moved.")

def find_duplicates(directory):
    """Finds duplicate files within the given directory based on MD5 hash."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return {}

    print(f"\nScanning '{directory}' for duplicates...")
    hashes = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = calculate_file_hash(filepath)
                hashes[file_hash].append(filepath)
            except Exception as e:
                print(f"  Error hashing '{filepath}': {e}")
    
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    if duplicates:
        print("\nFound duplicates:")
        for file_hash, paths in duplicates.items():
            print(f"  Hash: {file_hash}")
            for p in paths:
                print(f"    - {p}")
    else:
        print("\nNo duplicates found.")
        
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Scavenger's Stash Organizer: Categorize and find duplicates in your digital hoard."
    )
    parser.add_argument(
        'source_directory', 
        help='The directory containing files to organize.'
    )
    parser.add_argument(
        'destination_directory', 
        help='The directory where organized files will be placed.'
    )
    
    args = parser.parse_args()
    
    organize_stash(args.source_directory, args.destination_directory)
    find_duplicates(args.destination_directory)

if __name__ == '__main__':
    main()
