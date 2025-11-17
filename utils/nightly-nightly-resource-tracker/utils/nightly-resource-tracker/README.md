# Nightly Resource Tracker

## Overview
The `nightly-resource-tracker` is a simple, self-contained command-line utility designed to help you keep tabs on your vital survival resources. Whether you're stockpiling for the apocalypse or just organizing your pantry, this tool provides a straightforward way to add, remove, and list items and their quantities in a persistent text file.

It's perfect for those who prefer a minimalist, text-based inventory system that's easy to inspect and manage.

## Features
*   **Add Resources**: Increment the quantity of an existing resource or add a new one.
*   **Remove Resources**: Decrement the quantity of an existing resource. If the quantity drops to zero or below, the resource is removed from the inventory.
*   **List Resources**: Display all tracked resources and their current quantities.
*   **Persistent Storage**: All data is stored in a `resources.txt` file in the utility's directory, making it easy to back up or inspect manually.

## Installation
This utility is written in Python 3.11 and requires no external dependencies beyond the standard library. Simply place the `src/tracker.py` file in a directory and run it directly.

## Usage
Navigate to the `utils/nightly-resource-tracker/src/` directory in your terminal.

### Add a resource
To add or update a resource, use the `add` command:

```bash
python tracker.py add "Water Gallons" 5
python tracker.py add "Canned Beans" 12
```
If "Water Gallons" already exists, its quantity will be increased by 5. Otherwise, it will be added with a quantity of 5.

### Remove a resource
To remove a quantity of a resource, use the `remove` command:

```bash
python tracker.py remove "Water Gallons" 2
```
If 2 "Water Gallons" are removed, the quantity will decrease. If the quantity drops to 0 or less, the item is removed from the list.

### List all resources
To see your current inventory, use the `list` command:

```bash
python tracker.py list
```

Example output:
```
--- Current Resources ---
Water Gallons: 3
Canned Beans: 12
First Aid Kits: 1
-------------------------
```

## Resource File Format
The `resources.txt` file is a simple key-value store, with each resource on a new line in the format `Resource Name=Quantity`.

Example `resources.txt`:
```
Water Gallons=3
Canned Beans=12
First Aid Kits=1
```
