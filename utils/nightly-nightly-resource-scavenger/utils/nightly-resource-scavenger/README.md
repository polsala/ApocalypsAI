# Nightly Resource Scavenger

A crucial CLI utility for the discerning survivor, the Nightly Resource Scavenger helps you keep track of your precious scavenged goods in a world gone wild. No more losing count of your canned beans or duct tape!

## Features

*   **Add Resources**: Quickly log new items and their quantities.
*   **Remove Resources**: Update your inventory when items are consumed or traded.
*   **List Inventory**: See a comprehensive overview of all your current supplies.
*   **Clear Inventory**: Start fresh when you move to a new hideout or face a catastrophic loss.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

1.  Navigate to the `utils/nightly-resource-scavenger/src` directory.
2.  Make the script executable: `chmod +x scavenger.py`

## Usage

All commands are run via the `scavenger.py` script. The resource data is stored in a `resources.json` file within the same directory as the script.

### Add Resources

Add a new item or increase the quantity of an existing one.

```bash
./scavenger.py add "Canned Beans" 5
# Output: Scavenged 5 units of 'Canned Beans'. Inventory updated, survivor!
```

### Remove Resources

Decrease the quantity of an existing item. If the quantity drops to zero or below, the item is removed from the inventory.

```bash
./scavenger.py remove "Canned Beans" 2
# Output: Consumed 2 units of 'Canned Beans'. Inventory updated, survivor!
```

### List Inventory

Display all items and their current quantities.

```bash
./scavenger.py list
# Output:
# --- Current Inventory ---
# Canned Beans: 3
# Duct Tape: 1
# Water Purifier Tablets: 10
# -------------------------
# Stay vigilant, survivor!
```

### Clear Inventory

Wipe your entire inventory. Use with caution!

```bash
./scavenger.py clear
# Output: Inventory wiped clean. A fresh start, or a grave loss? Only time will tell.
```

## Development

To run tests:

```bash
python3 -m unittest tests/test_scavenger.py
```
