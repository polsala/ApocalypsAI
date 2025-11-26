# Nightly Resource Tracker

## Overview

The `nightly-resource-tracker` is a simple, command-line utility designed to help you keep tabs on your precious supplies in a world where every scrap counts. Whether it's water rations, scavenged batteries, or that last can of irradiated beans, this tool ensures you know exactly what you have and how much.

It stores your resources in a plain text file (`resources.txt`) in the current directory, making it easy to inspect and even manually edit if needed.

## Usage

To run the tracker, navigate to the `src` directory and execute `python tracker.py` followed by a command.

### Commands:

*   `add <resource_name> <quantity>`: Adds a specified quantity of a resource. If the resource already exists, its quantity will be increased.
*   `remove <resource_name> <quantity>`: Removes a specified quantity of a resource. If the quantity to remove exceeds the available amount, an error will be displayed.
*   `list`: Displays all currently tracked resources and their quantities.

### Examples:

```bash
# Add 5 units of 'water'
python tracker.py add water 5

# Add 2 units of 'canned_food'
python tracker.py add canned_food 2

# List all resources
python tracker.py list
# Expected output:
# --- Current Resources ---
# canned_food: 2
# water: 5
# -------------------------

# Remove 1 unit of 'water'
python tracker.py remove water 1

# List again
python tracker.py list
# Expected output:
# --- Current Resources ---
# canned_food: 2
# water: 4
# -------------------------

# Try to remove more than available (will show an error)
python tracker.py remove water 10

# Add a new resource
python tracker.py add batteries 10

# List all resources
python tracker.py list
# Expected output:
# --- Current Resources ---
# batteries: 10
# canned_food: 2
# water: 4
# -------------------------
```

## Development

The utility is written in Python 3.11 and uses standard library features. Tests are located in `tests/test_tracker.py` and can be run using `python -m unittest tests/test_tracker.py` from the `utils/nightly-resource-tracker` directory.
