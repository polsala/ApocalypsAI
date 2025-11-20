# Nightly Rubble-Rouser Resource Tracker

## 📦 Overview

The Nightly Rubble-Rouser Resource Tracker is a simple command-line utility designed to help survivors (or particularly organized scavengers) keep tabs on their precious hoards of post-apocalyptic resources. Whether it's cans of irradiated beans, rolls of duct tape, or mysterious glowing fungi, this tracker ensures you always know what you have and how much. No more losing track of your last bottle cap!

## ✨ Features

*   **Add Resources**: Easily add new items and their quantities to your inventory.
*   **List Inventory**: View a comprehensive list of all your scavenged goods.
*   **Consume Resources**: Mark items as used, decrementing their count.
*   **Clear Stash**: Start fresh when you move to a new, less radioactive hideout.
*   **Persistent Storage**: Your inventory is saved to a local JSON file, so your hard-earned loot isn't lost after a system reboot (or a zombie attack).

## 🚀 Usage

Navigate to the `src/` directory and run `tracker.py` with the desired command.

```bash
# Add 5 cans of "Irradiated Beans"
python tracker.py add "Irradiated Beans" 5

# Add 2 rolls of "Duct Tape"
python tracker.py add "Duct Tape" 2

# List current inventory
python tracker.py list

# Consume 1 "Irradiated Beans"
python tracker.py consume "Irradiated Beans" 1

# Clear all resources
python tracker.py clear
```

### Commands:

*   `add <item_name> <quantity>`: Adds or updates the quantity of an item. `item_name` can be a string (use quotes for multi-word names), `quantity` must be a positive integer.
*   `list`: Displays all items and their current quantities.
*   `consume <item_name> <quantity>`: Decreases the quantity of an item. If the quantity drops to zero or below, the item is removed. `quantity` must be a positive integer.
*   `clear`: Empties the entire resource inventory.

## 🛠️ Development

The tracker uses a simple JSON file (`resources.json`) for persistence. Tests are located in `tests/test_tracker.py` and can be run using `pytest`.

```bash
# From the util's root directory:
pip install pytest
pytest tests/
```
