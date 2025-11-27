# Rubble-Rouser Resource Tracker

## Overview
In the desolate aftermath, every scrap counts! The `Rubble-Rouser Resource Tracker` is your essential companion for cataloging and managing the precious resources you scavenge. Whether it's irradiated canned goods, salvaged electronics, or purified water, keep a meticulous inventory to ensure your survival and prosperity in the new world.

This utility provides a simple command-line interface to add, remove, list, and summarize your resources, categorized for easy management.

## Features
*   **Add Resources**: Quickly add new items or increase the quantity of existing ones.
*   **Remove Resources**: Deduct items from your inventory, useful after crafting or consumption.
*   **List Inventory**: View all your resources, or filter by specific categories.
*   **Category Summary**: Get a quick overview of your total quantities per resource category.
*   **Persistent Storage**: Your inventory is saved to a local `resources.json` file.

## Installation
1.  Clone the ApocalypsAI repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility directory:
    ```bash
    cd utils/nightly-rubble-rouser-resource-tracker
    ```
3.  The utility is self-contained. You can run it directly using Python 3.11+.

## Usage
Run the `tracker.py` script with various commands:

```bash
python3 src/tracker.py <command> [arguments]
```

### Commands:

#### `add <name> <quantity> [category]`
Adds a new resource or increases the quantity of an existing one. If the category is not provided, it defaults to `misc`.

*   `<name>`: The name of the resource (e.g., "Canned Beans", "Copper Wire").
*   `<quantity>`: The amount to add (must be a positive integer).
*   `[category]`: Optional. A category for the resource (e.g., "food", "materials", "medicine").

**Examples:**
```bash
python3 src/tracker.py add "Canned Beans" 10 food
python3 src/tracker.py add "Purified Water" 5 hydration
python3 src/tracker.py add "Scrap Metal" 20 materials
python3 src/tracker.py add "First Aid Kit" 1 medicine
```

#### `remove <name> <quantity>`
Removes a specified quantity of a resource. If the quantity to remove exceeds what's available, it will remove all available and warn you.

*   `<name>`: The name of the resource to remove.
*   `<quantity>`: The amount to remove (must be a positive integer).

**Examples:**
```bash
python3 src/tracker.py remove "Canned Beans" 3
python3 src/tracker.py remove "Scrap Metal" 50 # Will remove all if less than 50 are present
```

#### `list [category]`
Lists all resources in your inventory, or filters by a specific category.

*   `[category]`: Optional. If provided, only resources from this category will be listed.

**Examples:**
```bash
python3 src/tracker.py list
python3 src/tracker.py list food
```

#### `summary`
Provides a summary of total quantities for each resource category.

**Example:**
```bash
python3 src/tracker.py summary
```

## Data Storage
Your resource inventory is stored in `resources.json` within the utility's directory. This file is automatically created and updated by the `tracker.py` script.
