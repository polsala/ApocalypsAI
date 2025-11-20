# Nightly Scavenger Salvage Sorter

## 📦 Overview

In the chaotic aftermath, every byte counts, and every file needs its place! The `Nightly Scavenger Salvage Sorter` is your trusty digital companion for bringing order to the digital rubble. Whether you're sifting through salvaged data drives or just trying to organize your pre-apocalypse downloads, this utility helps categorize files into logical 'salvage bins' based on their names and extensions.

Think of it as a digital sorting hat for your files, ensuring that your 'consumables' (e.g., recipes, survival guides) don't get mixed up with your 'tools' (e.g., scripts, utilities) or 'weapons' (e.g., that old Doom mod).

## ✨ Features

*   **Intelligent Categorization**: Uses a predefined set of keywords and file extensions to sort items into categories like `consumables`, `tools`, `electronics`, `materials`, `documents`, `weapons`, and `misc`.
*   **Dry Run Mode**: Preview how your files will be sorted before making any actual changes.
*   **Self-Contained**: Written in Python, easy to run and integrate into your nightly routines.

## 🚀 Usage

To run the sorter, navigate to the utility's directory and execute the `sorter.py` script. For actual use, you'll typically provide a source directory and a destination base directory.

```bash
python3 src/sorter.py --source /path/to/your/salvage --destination /path/to/your/bins
```

### Command Line Arguments (Planned for future expansion, currently uses hardcoded example paths in `main()`):

*   `--source <directory>`: The directory containing files to be sorted.
*   `--destination <directory>`: The base directory where category subfolders will be created.
*   `--dry-run`: If present, the utility will only print what it *would* do, without moving any files or creating directories.

### Example (as implemented in `src/sorter.py`'s `main` function):

```python
# In src/sorter.py, the main() function demonstrates this:
# It creates dummy files in 'salvage_pile' and sorts them into 'salvage_bins'.
# You can modify the main() function or call sort_files_in_directory directly.

# Example of direct function call:
from src.sorter import load_rules, sort_files_in_directory

rules = load_rules()
source_path = "./my_unsorted_data"
dest_path = "./my_sorted_bins"

# Perform a dry run
sort_files_in_directory(source_path, dest_path, rules, dry_run=True)

# Perform actual sorting
sort_files_in_directory(source_path, dest_path, rules, dry_run=False)
```

## ⚙️ Configuration (Rules)

The categorization rules are currently hardcoded within the `load_rules()` function in `src/sorter.py`. You can modify this function to customize categories and keywords to better suit your specific salvage needs.

```python
def load_rules():
    return {
        "consumables": ["food", "water", "ration", "can", "bottle", "medkit", "firstaid"],
        "tools": ["wrench", "hammer", "saw", "screwdriver", "axe", "knife", "toolkit"],
        "electronics": ["radio", "battery", "circuit", "wire", "chip", "device", "tablet"],
        "materials": ["scrap", "metal", "wood", "plastic", "fabric", "rope", "pipe"],
        "documents": ["map", "journal", "note", "book", "log", "schematic", "paper"],
        "weapons": ["gun", "ammo", "bow", "arrow", "blade", "rifle", "pistol"],
        "misc": [] # Catch-all for anything else
    }
```

## 🧪 Testing

Tests are located in `tests/test_sorter.py` and can be run using `unittest`:

```bash
python3 -m unittest tests/test_sorter.py
```

All tests are deterministic and use mocks to simulate file system operations, ensuring they run offline and reliably.
