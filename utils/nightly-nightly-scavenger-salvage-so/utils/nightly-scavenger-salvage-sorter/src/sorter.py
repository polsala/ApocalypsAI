import os
import shutil
import argparse
from typing import Dict, List, Tuple

def load_rules() -> Dict[str, List[str]]:
    """
    Loads predefined categorization rules.
    In a real-world scenario, this might load from a config file (e.g., JSON, YAML).
    """
    return {
        "consumables": ["food", "water", "ration", "can", "bottle", "medkit", "firstaid"],
        "tools": ["wrench", "hammer", "saw", "screwdriver", "axe", "knife", "toolkit"],
        "electronics": ["radio", "battery", "circuit", "wire", "chip", "device", "tablet"],
        "materials": ["scrap", "metal", "wood", "plastic", "fabric", "rope", "pipe"],
        "documents": ["map", "journal", "note", "book", "log", "schematic", "paper"],
        "weapons": ["gun", "ammo", "bow", "arrow", "blade", "rifle", "pistol"],
        "misc": [] # Catch-all
    }

def get_file_extension(filename: str) -> str:
    """Extracts the file extension."""
    return os.path.splitext(filename)[1].lower()

def categorize_item(item_name: str, rules: Dict[str, List[str]]) -> str:
    """
    Categorizes an item based on its name and predefined rules.
    Prioritizes specific keywords over general ones.
    """
    item_name_lower = item_name.lower()
    
    # Check for specific keywords
    for category, keywords in rules.items():
        for keyword in keywords:
            if keyword in item_name_lower:
                return category
    
    # Check for common file extensions if it looks like a file
    ext = get_file_extension(item_name)
    if ext:
        if ext in [".txt", ".md", ".pdf", ".doc", ".docx", ".odt", ".rtf"]:
            return "documents"
        if ext in [".jpg", ".png", ".gif", ".bmp", ".jpeg", ".webp", ".tiff"]:
            return "misc" # Could be "records" or "visuals"
        if ext in [".mp3", ".wav", ".ogg", ".flac", ".m4a"]:
            return "misc" # Could be "entertainment"
        if ext in [".py", ".sh", ".exe", ".bin", ".zip", ".tar.gz", ".rar", ".7z", ".iso"]:
            return "electronics" # Or "software" / "archives"
    
    return "misc" # Default category

def sort_files_in_directory(
    source_dir: str, 
    destination_base_dir: str, 
    rules: Dict[str, List[str]],
    dry_run: bool = False
) -> List[Tuple[str, str, str]]:
    """
    Scans a source directory, categorizes files, and (optionally) moves them
    to subdirectories within the destination_base_dir.
    
    Returns a list of (original_path, suggested_category, new_path_if_moved).
    """
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return []

    if not os.path.exists(destination_base_dir) and not dry_run:
        os.makedirs(destination_base_dir)
        print(f"Created destination base directory: {destination_base_dir}")

    sorted_actions = []
    
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            category = categorize_item(filename, rules)
            
            target_category_dir = os.path.join(destination_base_dir, category)
            target_file_path = os.path.join(target_category_dir, filename)
            
            if not dry_run:
                if not os.path.exists(target_category_dir):
                    os.makedirs(target_category_dir)
                    print(f"Created category directory: {target_category_dir}")
                
                try:
                    shutil.move(file_path, target_file_path)
                    print(f"Moved '{filename}' to '{category}/'")
                    sorted_actions.append((file_path, category, target_file_path))
                except Exception as e:
                    print(f"Error moving '{filename}': {e}")
                    sorted_actions.append((file_path, category, f"ERROR: {e}"))
            else:
                print(f"[DRY RUN] Would move '{filename}' to '{category}/'")
                sorted_actions.append((file_path, category, target_file_path))
                
    return sorted_actions

def main():
    """
    Main entry point for the utility.
    Parses command-line arguments or demonstrates with example directories.
    """
    parser = argparse.ArgumentParser(description="Scavenger's Salvage Sorter: Organize your digital rubble.")
    parser.add_argument('--source', type=str, help='Source directory containing files to sort.')
    parser.add_argument('--destination', type=str, help='Base directory where sorted categories will be created.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without moving files.')
    
    args = parser.parse_args()

    print("--- Scavenger's Salvage Sorter ---")
    
    rules = load_rules()

    if args.source and args.destination:
        print(f"\nSorting from '{args.source}' to '{args.destination}' (Dry Run: {args.dry_run}):")
        sort_files_in_directory(args.source, args.destination, rules, dry_run=args.dry_run)
    else:
        print("No source or destination provided. Running demonstration mode.")
        # Demonstration mode with dummy files and cleanup
        source_dir = "salvage_pile_demo"
        destination_base_dir = "salvage_bins_demo"
        
        # Clean up previous runs
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
        if os.path.exists(destination_base_dir):
            shutil.rmtree(destination_base_dir)

        os.makedirs(source_dir, exist_ok=True)
        
        # Create some dummy files
        with open(os.path.join(source_dir, "rusty_wrench.txt"), "w") as f: f.write("tool")
        with open(os.path.join(source_dir, "canned_beans.dat"), "w") as f: f.write("food")
        with open(os.path.join(source_dir, "broken_radio.log"), "w") as f: f.write("electronics")
        with open(os.path.join(source_dir, "torn_map.pdf"), "w") as f: f.write("document")
        with open(os.path.join(source_dir, "pile_of_scrap_metal.bin"), "w") as f: f.write("material")
        with open(os.path.join(source_dir, "unknown_item.jpg"), "w") as f: f.write("misc")
        with open(os.path.join(source_dir, "laser_pistol.txt"), "w") as f: f.write("weapon")
        with open(os.path.join(source_dir, "firstaid_manual.md"), "w") as f: f.write("consumable")

        print(f"\nCreated dummy files in '{source_dir}':")
        for f in os.listdir(source_dir):
            print(f"- {f}")

        print(f"\nPerforming dry run sorting from '{source_dir}' to '{destination_base_dir}':")
        sort_files_in_directory(source_dir, destination_base_dir, rules, dry_run=True)
        
        print(f"\nPerforming actual sorting from '{source_dir}' to '{destination_base_dir}':")
        sort_files_in_directory(source_dir, destination_base_dir, rules, dry_run=False)
        
        print("\n--- Sorting Complete ---")
        print(f"Check '{destination_base_dir}' for sorted files.")

        # Clean up after demonstration
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
        if os.path.exists(destination_base_dir):
            shutil.rmtree(destination_base_dir)


if __name__ == "__main__":
    main()
