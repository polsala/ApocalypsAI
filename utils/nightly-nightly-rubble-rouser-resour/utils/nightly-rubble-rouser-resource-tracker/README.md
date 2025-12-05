# Nightly Rubble-Rouser Resource Tracker

## Overview

The `nightly-rubble-rouser-resource-tracker` is a simple command-line utility designed to help survivors keep tabs on their precious scavenged resources. In a world where every can of beans and every roll of duct tape counts, this tool ensures you always know what you have, and how much. No more guessing if you have enough "Shiny Bits" for that critical repair!

## Features

*   **Add Resources**: Easily log new items and their quantities.
*   **Remove Resources**: Update your inventory when items are used or traded.
*   **List Resources**: Get a clear overview of all your current supplies.
*   **Persistent Storage**: Your inventory is saved to a local JSON file, so your hard-won gains are never lost.

## Installation

This utility is self-contained and requires Python 3.8+ (tested with 3.11). No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/nightly-rubble-rouser-resource-tracker/` directory.
2.  The main script is `src/tracker.py`.

## Usage

Run the `tracker.py` script directly from its `src/` directory.

```bash
python src/tracker.py <command> [arguments]
```

### Commands:

*   **`add <item_name> <quantity>`**: Adds or updates the quantity of an item.
    *   `item_name`: The name of the resource (e.g., "Canned Beans", "Scrap Metal"). Use quotes for names with spaces.
    *   `quantity`: A positive integer representing the amount.
    *   Example: `python src/tracker.py add "Canned Beans" 5`

*   **`remove <item_name> <quantity>`**: Decreases the quantity of an item. If the quantity drops to 0 or below, the item is removed.
    *   `item_name`: The name of the resource.
    *   `quantity`: A positive integer representing the amount to remove.
    *   Example: `python src/tracker.py remove "Canned Beans" 2`

*   **`list`**: Displays all currently tracked resources and their quantities.
    *   Example: `python src/tracker.py list`

## Examples

```bash
# Add some initial supplies
python src/tracker.py add "Purified Water" 10
python src/tracker.py add "Medical Kits" 3
python src/tracker.py add "Scrap Metal" 50

# Check your inventory
python src/tracker.py list

# Use some water
python src/tracker.py remove "Purified Water" 3

# Add more scrap
python src/tracker.py add "Scrap Metal" 15

# Check again
python src/tracker.py list
```

## Data Storage

The resource data is stored in a JSON file named `resources.json` in the same directory as `tracker.py`.
