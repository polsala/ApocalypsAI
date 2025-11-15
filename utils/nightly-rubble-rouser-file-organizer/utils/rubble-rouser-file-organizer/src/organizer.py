import os
import shutil
import sys
from collections import defaultdict

# Define file categories and their associated extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".sh", ".json", ".xml", ".yml", ".yaml"],
    "Executables": [".exe", ".dmg", ".app", ".deb", ".rpm"],
    "Others": [] # Catch-all for uncategorized files
}

# Reverse mapping for quick lookup
EXTENSION_MAP = {}
for category, extensions in FILE_CATEGORIES.items():
    for ext in extensions:
        EXTENSION_MAP[ext.lower()] = category

def get_category(filename):
    """Determines the category of a file based on its extension."""
    _, ext = os.path.splitext(filename)
    return EXTENSION_MAP.get(ext.lower(), "Others")

def organize_directory(source_dir):
    """Organizes files in the given source directory into categorized subfolders."""
    if not os.path.isdir(source_dir):
        print(f"[Rubble-Rouser] ERROR: Source directory '{source_dir}' not found. Aborting salvage operation.")
        return

    print(f"[Rubble-Rouser] Initiating salvage operation in '{source_dir}'...")

    # Create target subdirectories
    for category in FILE_CATEGORIES:
        target_path = os.path.join(source_dir, category)
        os.makedirs(target_path, exist_ok=True)
        print(f"[Rubble-Rouser] Ensuring 'Zone {category}' is ready for new finds.")

    files_moved = defaultdict(int)
    files_skipped = 0

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        if os.path.isfile(item_path):
            category = get_category(item)
            target_category_dir = os.path.join(source_dir, category)
            target_file_path = os.path.join(target_category_dir, item)

            # If the file is already in its correct category folder, skip it
            if os.path.abspath(item_path) == os.path.abspath(target_file_path):
                print(f"[Rubble-Rouser] Relic '{item}' already in its designated 'Zone {category}'. Skipping.")
                files_skipped += 1
                continue

            try:
                # Check if a file with the same name already exists in the target to prevent overwrite
                if os.path.exists(target_file_path):
                    print(f"[Rubble-Rouser] WARNING: Duplicate relic '{item}' found in 'Zone {category}'. Skipping to prevent overwrite.")
                    files_skipped += 1
                    continue

                shutil.move(item_path, target_file_path)
                print(f"[Rubble-Rouser] Salvaged '{item}' and moved to 'Zone {category}'.")
                files_moved[category] += 1
            except OSError as e:
                print(f"[Rubble-Rouser] ERROR: Failed to move '{item}': {e}. Skipping.")
                files_skipped += 1
        elif os.path.isdir(item_path) and item not in FILE_CATEGORIES: # Ignore user-created subdirectories that are not category dirs
            print(f"[Rubble-Rouser] Discovered uncharted territory '{item}'. Ignoring for now.")
            files_skipped += 1
        # If it's a directory and it IS one of our categories, we also ignore it (it was created by us or already existed)

    print("\n[Rubble-Rouser] Salvage operation complete!")
    if files_moved:
        print("--- Salvage Report ---")
        for category, count in files_moved.items():
            print(f"  - {count} relics secured in 'Zone {category}'.")
    if files_skipped > 0:
        print(f"  - {files_skipped} items left untouched (either duplicates, directories, or errors).")
    print("----------------------")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organizer.py <directory_path>")
        sys.exit(1)

    source_directory = sys.argv[1]
    organize_directory(source_directory)
