import os
import shutil
import argparse
import sys

# Define file categories and their associated extensions
FILE_CATEGORIES = {
    "Documents": [".txt", ".pdf", ".doc", ".docx", ".odt", ".rtf", ".md"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Executables": [".exe", ".sh", ".bat", ".app"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rb"],
}

def get_category(filename):
    """Determines the category of a file based on its extension."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"

def sort_stash(source_dir, destination_dir):
    """Sorts files from source_dir into categorized subdirectories in destination_dir."""
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.", file=sys.stderr)
        return False

    os.makedirs(destination_dir, exist_ok=True)
    print(f"Sorting files from '{source_dir}' to '{destination_dir}'...")

    files_processed = 0
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)

        if os.path.isfile(source_path):
            category = get_category(item)
            category_dir = os.path.join(destination_dir, category)
            os.makedirs(category_dir, exist_ok=True)

            destination_path = os.path.join(category_dir, item)
            
            # Handle duplicate filenames by appending a counter
            base_name, ext = os.path.splitext(item)
            counter = 1
            while os.path.exists(destination_path):
                new_item_name = f"{base_name}_{counter}{ext}"
                destination_path = os.path.join(category_dir, new_item_name)
                counter += 1

            try:
                shutil.move(source_path, destination_path)
                print(f"  Moved '{item}' to '{category}/{os.path.basename(destination_path)}'")
                files_processed += 1
            except Exception as e:
                print(f"  Error moving '{item}': {e}", file=sys.stderr)
        elif os.path.isdir(source_path):
            print(f"  Skipping directory '{item}'")

    print(f"Sorting complete. {files_processed} files processed.")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Organize your digital 'scavenged goods' by sorting files into categorized subdirectories."
    )
    parser.add_argument(
        "--source", 
        required=True, 
        help="The path to the directory containing the files to sort."
    )
    parser.add_argument(
        "--destination", 
        help="The path where the sorted category folders will be created. Defaults to 'sorted_stash' inside the source directory."
    )

    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    destination_dir = os.path.abspath(args.destination) if args.destination else os.path.join(source_dir, "sorted_stash")

    if not sort_stash(source_dir, destination_dir):
        sys.exit(1)

if __name__ == "__main__":
    main()
