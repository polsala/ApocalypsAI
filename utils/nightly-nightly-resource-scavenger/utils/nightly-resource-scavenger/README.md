# Nightly Resource Scavenger

A humble command-line utility for the discerning post-apocalyptic survivor (or just anyone who needs to keep track of things). The Nightly Resource Scavenger helps you catalog your precious finds, track quantities, and remember where you stashed them. No more losing that last can of irradiated beans!

## Features

*   **Add Resources**: Log new items you've scavenged.
*   **Update Quantities**: Adjust counts as you use or find more.
*   **Remove Resources**: Declutter your inventory when items are gone.
*   **List Inventory**: See everything you've got at a glance.
*   **Persistent Storage**: Your inventory is saved to a local JSON file.

## Installation

This utility is self-contained and requires Python 3.11+.

1.  Navigate to the `utils/nightly-resource-scavenger/` directory.
2.  Run the script directly.

## Usage

The `scavenger.py` script uses a `resources.json` file in the same directory to store your inventory.

### Add a resource

```bash
python src/scavenger.py add --name "Irradiated Beans" --quantity 5 --location "Pantry Shelf 3"
python src/scavenger.py add --name "Duct Tape" --quantity 1 --location "Toolbox"
```

### Update a resource's quantity

```bash
python src/scavenger.py update --name "Irradiated Beans" --quantity 4
```

### Remove a resource

```bash
python src/scavenger.py remove --name "Duct Tape"
```

### List all resources

```bash
python src/scavenger.py list
```

## Example Output

```
$ python src/scavenger.py list
--- Current Inventory ---
Name: Irradiated Beans, Quantity: 4, Location: Pantry Shelf 3
Name: Water Purifier Tablets, Quantity: 10, Location: First Aid Kit
-------------------------
```

## Development

To run tests:

```bash
python -m unittest tests/test_scavenger.py
```
