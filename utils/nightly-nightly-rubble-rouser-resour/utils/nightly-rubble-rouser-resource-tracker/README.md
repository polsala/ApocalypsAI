# Rubble-Rouser Resource Tracker

A whimsical-yet-useful command-line utility for tracking your scavenged resources across various stashes and locations in a post-apocalyptic world. Keep tabs on your water, food, ammo, and other vital supplies, and get alerts when stock runs low!

## Features

*   **Stash Management**: Organize resources by specific locations (e.g., "Garage", "Old Bunker", "Hidden Cache").
*   **Resource Tracking**: Add, update, and remove quantities of any item.
*   **Comprehensive Summary**: Get an overview of all your resources across all stashes, including global totals.
*   **Low Stock Alerts**: Be notified when critical supplies fall below a configurable threshold.

## Installation

This utility is a single Python script and requires no special installation beyond having Python 3.6+ installed.

1.  Navigate to the `src/` directory:
    ```bash
    cd utils/nightly-rubble-rouser-resource-tracker/src
    ```
2.  You can then run the script directly.

## Usage

The `tracker.py` script uses subcommands for different operations.

### Add Resources

To add a new resource or increase the quantity of an existing one:

```bash
python tracker.py add <stash_name> <item_name> <quantity>
```

**Examples:**
```bash
python tracker.py add "Garage" "Water Bottle" 10
python tracker.py add "Old Bunker" "Canned Beans" 5
python tracker.py add "Garage" "Water Bottle" 3 # Adds 3 more to existing 10
```

### Remove Resources

To decrease the quantity of a resource or remove it entirely if the quantity drops to zero or below:

```bash
python tracker.py remove <stash_name> <item_name> <quantity>
```

**Examples:**
```bash
python tracker.py remove "Garage" "Water Bottle" 2
python tracker.py remove "Old Bunker" "Canned Beans" 5 # Removes all 5
```

### Get Summary

To view a comprehensive summary of all resources across all stashes:

```bash
python tracker.py summary
```

**Example Output:**
```
--- Resource Summary ---

Stash: Garage
  - Water Bottle: 11
  - Duct Tape: 2

Stash: Old Bunker
  - Canned Beans: 3
  - Medkit: 1

--- Global Totals ---
  - Canned Beans: 3
  - Duct Tape: 2
  - Medkit: 1
  - Water Bottle: 11
```

### Get Low Stock Alerts

To check for resources that are below a specified quantity threshold:

```bash
python tracker.py alerts [--threshold <number>]
```

The default threshold is `5`.

**Examples:**
```bash
python tracker.py alerts
python tracker.py alerts --threshold 10
```

**Example Output:**
```
--- Low Stock Alerts ---
LOW STOCK: Duct Tape in Garage has only 2 left (threshold: 5)
LOW STOCK: Medkit in Old Bunker has only 1 left (threshold: 5)
```

## Data Storage

The utility stores its data in a `resources.json` file located in the same directory as `tracker.py`. This file is automatically created and managed by the script.

**Example `resources.json` structure:**
```json
{
    "Garage": {
        "Water Bottle": 11,
        "Duct Tape": 2
    },
    "Old Bunker": {
        "Canned Beans": 3,
        "Medkit": 1
    }
}
```
