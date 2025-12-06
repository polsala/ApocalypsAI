# Apocalypse Resource Tracker

## Overview

The `apocalypse-resource-tracker` is a simple, self-contained command-line utility designed to help you manage your vital resources. Whether you're stockpiling for the end of days, organizing your emergency pantry, or just keeping tabs on your gaming inventory, this tool provides a straightforward way to track items, quantities, expiration dates, and storage locations.

It's built with Python and stores your data in a human-readable JSON file, making it easy to inspect and manage.

## Features

*   **Add Items**: Quickly add new resources with a name, quantity, and optional details like expiration date and location.
*   **Consume Items**: Decrement quantities as you use or find items.
*   **List Inventory**: View your current stock, with warnings for expired or low-stock items.
*   **Persistent Storage**: Data is automatically saved to a local JSON file.

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the `utils/apocalypse-resource-tracker/` directory.
2.  You can run it directly using `python src/tracker.py`.

For convenience, you might want to create an alias or a symlink:

```bash
# Example for Linux/macOS
ln -s "$(pwd)/src/tracker.py" /usr/local/bin/tracker
# Make sure /usr/local/bin is in your PATH
```

## Usage

All commands are run via `python src/tracker.py <command> [options]`.

### Add an item

```bash
python src/tracker.py add "Canned Beans" 12 --expires "2025-12-31" --location "Pantry Shelf 3"
python src/tracker.py add "Water Purifier Tablets" 50
```

*   `--expires YYYY-MM-DD`: Optional expiration date.
*   `--location "Someplace"`: Optional storage location.

### Consume an item

```bash
python src/tracker.py consume "Canned Beans" 1
python src/tracker.py consume "Water Purifier Tablets" 5
```

### List inventory

```bash
python src/tracker.py list
```

This will display your current inventory, highlighting items that are expired or low on stock.

### Data File

The tracker stores its data in a file named `resources.json` in the same directory as `tracker.py` by default. You can inspect or manually edit this file if needed (though it's recommended to use the CLI for consistency).

```json
[
  {
    "name": "Canned Beans",
    "quantity": 11,
    "expires": "2025-12-31",
    "location": "Pantry Shelf 3"
  },
  {
    "name": "Water Purifier Tablets",
    "quantity": 45,
    "expires": null,
    "location": null
  }
]
```
