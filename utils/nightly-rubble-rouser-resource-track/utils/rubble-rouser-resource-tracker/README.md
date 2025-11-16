# Rubble-Rouser Resource Tracker

A vital utility for the discerning scavenger, the Rubble-Rouser Resource Tracker helps you keep tabs on your precious finds across the desolate landscape. Never lose count of your canned goods, spare parts, or shiny trinkets again!

## Features

*   **Add Resources**: Easily log new items and their quantities.
*   **Update Quantities**: Adjust stock levels as you consume or discover more.
*   **List Inventory**: Get a clear overview of all your scavenged treasures.
*   **Persistent Storage**: Your inventory is saved to a local file, so your hard-earned data survives even the harshest digital storms.

## Usage

The tracker operates via the command line.

### Prerequisites

*   Python 3.8+

### Running the Tracker

Navigate to the `src` directory and run `tracker.py` with the desired command.

```bash
# Add a new resource or add to existing quantity
python tracker.py add "Canned Beans" 5
python tracker.py add "Scrap Metal" 20

# Set the quantity of an existing resource
python tracker.py update "Canned Beans" 3 # Sets quantity to 3

# Remove a resource entirely
python tracker.py remove "Scrap Metal"

# List all resources in your inventory
python tracker.py list

# Specify a custom inventory file (optional, defaults to 'inventory.json')
python tracker.py --file my_stash.json add "Water Purifier" 1
```

## Example

```bash
$ python tracker.py add "Canned Beans" 5
Added/Updated 'Canned Beans': 5 units.
$ python tracker.py add "Duct Tape" 2
Added/Updated 'Duct Tape': 2 units.
$ python tracker.py list
--- Current Inventory ---
Canned Beans: 5
Duct Tape: 2
-------------------------
$ python tracker.py update "Canned Beans" 3
Added/Updated 'Canned Beans': 3 units.
$ python tracker.py list
--- Current Inventory ---
Canned Beans: 3
Duct Tape: 2
-------------------------
$ python tracker.py remove "Duct Tape"
Removed 'Duct Tape' from inventory.
$ python tracker.py list
--- Current Inventory ---
Canned Beans: 3
-------------------------
```
