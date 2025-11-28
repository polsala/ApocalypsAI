# Nightly Resource Tracker

A simple, robust command-line utility for managing your scavenged resources in the wasteland. Keep tabs on your precious supplies, from purified water to rusty wrenches, ensuring you're always prepared for the next challenge.

## Features

*   **Add Resources**: Easily add new items or increase the quantity of existing ones.
*   **Remove Resources**: Decrease quantities or remove items entirely when consumed or lost.
*   **List Inventory**: View your entire inventory at a glance, with current quantities.
*   **Persistent Storage**: Your inventory is saved to a local `inventory.json` file, so your progress is never lost.

## Installation

This utility is self-contained. Simply navigate to the `utils/nightly-resource-tracker/src` directory.

## Usage

All commands are run via `python3 tracker.py` followed by the desired action and arguments.

### Add an item

To add a new item or increase the quantity of an existing one:

```bash
python3 src/tracker.py add --item "Purified Water" --quantity 5
python3 src/tracker.py add --item "Canned Beans" --quantity 12
```

### Remove an item

To remove a specific quantity of an item. If the quantity drops to zero or below, the item is removed from the inventory.

```bash
python3 src/tracker.py remove --item "Purified Water" --quantity 2
```

### List all items

To view your current inventory:

```bash
python3 src/tracker.py list
```

### Examples

```bash
# Add some initial supplies
python3 src/tracker.py add --item "Medical Kit" --quantity 1
python3 src/tracker.py add --item "Scrap Metal" --quantity 50
python3 src/tracker.py add --item "Rope" --quantity 10

# Check your inventory
python3 src/tracker.py list

# Use some scrap metal
python3 src/tracker.py remove --item "Scrap Metal" --quantity 15

# Add more rope found on a scavenging run
python3 src/tracker.py add --item "Rope" --quantity 5

# Check again
python3 src/tracker.py list
```
