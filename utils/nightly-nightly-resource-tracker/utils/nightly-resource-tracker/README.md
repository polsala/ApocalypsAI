# Rubble-Rouser Resource Tracker

## Overview

In the ever-unpredictable landscape of the post-apocalypse, keeping tabs on your vital supplies is paramount. The `Rubble-Rouser Resource Tracker` is your trusty digital ledger, designed to help you manage your inventory of essential resources, set low-stock thresholds, and get timely alerts before you run out of crucial items like 'Quantum Quake Quenchers' or 'Gloom-Glimmer Goggles'.

This utility is a self-contained Python script that stores your resource data in a simple JSON file, making it easy to integrate into your nightly survival routines.

## Features

*   **Add/Update Resources**: Easily add new items to your inventory or adjust quantities.
*   **Set Thresholds**: Define a low-stock threshold for each resource to receive warnings.
*   **Quantity Management**: Increase or decrease resource counts with a single command.
*   **Status Reports**: Get a quick overview of all your resources, indicating if they are 'OK' or 'LOW'.
*   **Persistent Storage**: All data is saved to a JSON file, so your inventory is always up-to-date.

## Installation

This utility is a standalone Python script. No special installation beyond having Python 3.11+ is required.

```bash
# Navigate to the utility directory
cd utils/nightly-resource-tracker/

# Run commands directly
python3 src/tracker.py --help
```

## Usage

The `tracker.py` script uses subcommands for different operations.

### 1. Add or Update a Resource

Use the `add` command to introduce a new resource or update an existing one's initial quantity and threshold.

```bash
python3 src/tracker.py add "Water Purifiers" 5 --threshold 2
python3 src/tracker.py add "Canned Beans" 30 --threshold 10
```

### 2. Update Resource Quantity

Use the `update` command to change the quantity of an existing resource. Use positive numbers to add and negative numbers to remove.

```bash
# Consume 1 Water Purifier
python3 src/tracker.py update "Water Purifiers" -1

# Find 5 more Canned Beans
python3 src/tracker.py update "Canned Beans" 5
```

### 3. Set Low-Stock Threshold

Adjust the warning threshold for a resource using the `set-threshold` command.

```bash
python3 src/tracker.py set-threshold "Water Purifiers" 1
```

### 4. List All Resources

Get a comprehensive list of all your tracked resources, their current quantities, thresholds, and status.

```bash
python3 src/tracker.py list
```

**Example Output:**

```
--- Current Resources ---
- Water Purifiers: 4 (Threshold: 1) - Status: OK
- Canned Beans: 35 (Threshold: 10) - Status: OK
- Medical Supplies: 8 (Threshold: 10) - Status: LOW
```

### Custom Data File

You can specify a different data file using the `--data-file` argument if you want to manage multiple inventories.

```bash
python3 src/tracker.py --data-file my_bunker_supplies.json add "Ammo (9mm)" 200 --threshold 50
```

## Development

To run tests, navigate to the `tests/` directory and execute `pytest` or `python3 -m unittest`.

```bash
cd utils/nightly-resource-tracker/tests/
python3 -m unittest test_tracker.py
```
