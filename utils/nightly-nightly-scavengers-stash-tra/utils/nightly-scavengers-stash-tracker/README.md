# Nightly Scavenger's Stash Tracker

A whimsical yet practical command-line utility for tracking your precious scavenged resources in the post-apocalyptic wasteland. Never lose track of your last can of beans or your dwindling supply of purified water again!

## Features

*   **Add/Update Items**: Easily add new items to your stash or update quantities of existing ones.
*   **List Stash**: View all items currently in your inventory.
*   **Remove Items**: Get rid of items you've used, traded, or lost to a pack of feral ghouls.
*   **Clear Stash**: Start fresh when you move to a new bunker or just want to forget your past scavenging failures.
*   **Persistent Storage**: Your stash is saved to a local JSON file, so your inventory persists between sessions.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies beyond standard library modules (`json`, `os`, `argparse`, `sys`).

1.  Navigate to the `utils/nightly-scavengers-stash-tracker/` directory.
2.  You can run the script directly: `python src/stash_tracker.py --help`

## Usage

The `stash_tracker.py` script uses subcommands for different operations.

### General Options

*   `--stash-file <path>`: (Optional) Specify a custom path for your stash JSON file. By default, it creates `scavenger_stash.json` in the current working directory.

### Commands

#### 1. Add or Update an Item

```bash
python src/stash_tracker.py add <item_name> <quantity>
```

*   `<item_name>`: The name of the item (e.g., "Water Bottle", "Scrap Metal"). Case-insensitive for internal tracking, but displays with original casing.
*   `<quantity>`: The amount to add. Can be negative to reduce the quantity.

**Examples:**

```bash
python src/stash_tracker.py add "Purified Water" 5
# Output: Added 'Purified Water' with quantity 5

python src/stash_tracker.py add "Scrap Metal" 10
# Output: Added 'Scrap Metal' with quantity 10

python src/stash_tracker.py add "Purified Water" 2
# Output: Updated 'Purified Water': new quantity is 7

python src/stash_tracker.py add "Scrap Metal" -3
# Output: Updated 'Scrap Metal': new quantity is 7
```

#### 2. List All Items

```bash
python src/stash_tracker.py list
```

**Example:**

```bash
python src/stash_tracker.py list
# Output:
# --- Your Scavenger's Stash ---
# - Purified Water: 7
# - Scrap Metal: 7
# ----------------------------
```

#### 3. Remove an Item

```bash
python src/stash_tracker.py remove <item_name>
```

*   `<item_name>`: The name of the item to remove.

**Example:**

```bash
python src/stash_tracker.py remove "Purified Water"
# Output: Removed 'Purified Water' from your stash.

python src/stash_tracker.py remove "Non-existent Item"
# Output: 'Non-existent Item' not found in your stash.
```

#### 4. Clear All Items

```bash
python src/stash_tracker.py clear
```

**Example:**

```bash
python src/stash_tracker.py clear
# Output: Your scavenger's stash has been cleared. A fresh start!
```

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_stash_tracker.py
```

All tests are deterministic and use mocks to simulate file system operations, ensuring they run offline and consistently.
