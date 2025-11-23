# Gloom-Gazer Gear Inventory Manager

## Overview

In the desolate aftermath, every piece of gear counts. The `Gloom-Gazer Gear Inventory Manager` is a simple, yet robust Python utility designed to help survivors meticulously track their precious resources. Whether it's a rusty can opener, a tattered map, or a dwindling supply of purified water, this tool ensures you always know what you have, where it is, and its current condition. No more frantic searches in the dark!

## Features

*   **Add Item**: Register new items with quantity, condition, and location.
*   **Remove Item**: Discard items (or mark them as lost).
*   **Update Item**: Adjust quantity, condition, or location of existing items.
*   **List Inventory**: View all items currently in your stash.
*   **Check Status**: Get a quick overview of your inventory, highlighting low stock or critical items.

## Usage

The utility operates via the command line. It stores inventory data in a `inventory.json` file in the same directory it's run from.

### Prerequisites

*   Python 3.6+

### Commands

```bash
# Add a new item
python src/inventory_manager.py add --name "Water Purifier Tablets" --quantity 50 --condition "New" --location "Backpack"

# Add another item
python src/inventory_manager.py add --name "Canned Beans" --quantity 12 --condition "Good" --location "Shelter Pantry"

# List all items
python src/inventory_manager.py list

# Update an item's quantity and condition
python src/inventory_manager.py update --name "Canned Beans" --quantity 10 --condition "Opened"

# Remove an item
python src/inventory_manager.py remove --name "Water Purifier Tablets"

# Check inventory status (e.g., low stock warnings)
python src/inventory_manager.py status
```

## Data Format

The inventory is stored in a `inventory.json` file, structured as a dictionary where keys are item names and values are dictionaries containing `quantity`, `condition`, and `location`.

Example `inventory.json`:

```json
{
  "Canned Beans": {
    "quantity": 10,
    "condition": "Opened",
    "location": "Shelter Pantry"
  },
  "First Aid Kit": {
    "quantity": 1,
    "condition": "Used",
    "location": "Medical Box"
  }
}
```
