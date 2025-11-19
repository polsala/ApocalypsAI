# Nightly Rubble-Rouser Resource Tracker

A whimsical-yet-useful command-line utility for the discerning survivor, designed to help you keep tabs on your precious hoard of post-apocalyptic resources. No more losing track of that last can of beans or that slightly-less-broken wrench!

## Features

*   **Add Resources**: Easily log new discoveries with quantity and location.
*   **Remove Resources**: Update your inventory as items are used or... misplaced.
*   **List All**: Get a comprehensive overview of everything you've got.
*   **Search**: Quickly find specific items across your inventory.
*   **Persistent Storage**: Your inventory is saved to a local JSON file, so your efforts aren't lost to the winds of chaos.

## Installation

This utility is self-contained and requires Python 3.8+ (compatible with 3.11).

1.  Navigate to the `utils/nightly-resource-tracker` directory.
2.  Run the script directly: `python src/tracker.py --help`

## Usage

The `tracker.py` script uses a simple command-line interface.

### Initialize (Optional, done automatically on first use)

The inventory file (`inventory.json`) will be created in the same directory as `src/tracker.py` if it doesn't exist.

### Add a resource

```bash
python src/tracker.py add "Canned Beans" 5 "Pantry Shelf"
python src/tracker.py add "Rusty Wrench" 1 "Toolbox"
```

### Remove a resource

This will decrement the quantity. If the quantity drops to 0 or below, the item is removed.

```bash
python src/tracker.py remove "Canned Beans" 2
```

### List all resources

```bash
python src/tracker.py list
```

### Search for a resource

```bash
python src/tracker.py search "beans"
```

## Inventory File

The inventory is stored in `inventory.json` in the same directory as `src/tracker.py`. It's a simple JSON array of objects:

```json
[
    {
        "name": "Canned Beans",
        "quantity": 3,
        "location": "Pantry Shelf"
    },
    {
        "name": "Rusty Wrench",
        "quantity": 1,
        "location": "Toolbox"
    }
]
```
