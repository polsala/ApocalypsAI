# Nightly Scavenger's Supply Ledger

## 📝 Overview

In the desolate wastes of the post-apocalypse, every scrap counts! The `Nightly Scavenger's Supply Ledger` is your trusty digital notebook for keeping track of all the precious loot you find. Whether it's a rusty can of beans, a half-broken flashlight, or a mysterious glowing rock, this utility helps you log, update, and manage your inventory.

It's a simple, self-contained Python command-line tool that stores your ledger data in a `scavenger_ledger.json` file, making it easy to keep tabs on your survival essentials.

## ✨ Features

*   **Add Items**: Quickly log new discoveries with quantity, condition, and notes.
*   **Update Items**: Modify existing item details as their status changes (e.g., using up supplies, repairing a tool).
*   **Remove Items**: Clear out items you've used, lost, or traded.
*   **List All Items**: Get a clear overview of your entire inventory.
*   **Portable**: All data is stored in a single JSON file, making it easy to back up or move.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+ (tested with Python 3.11)

### Running the Utility

Navigate to the `src` directory within the `nightly-scavenger-supply-ledger` folder.

```bash
cd utils/nightly-scavenger-supply-ledger/src
```

Then, run the `ledger.py` script with the desired command:

#### ➕ Add an Item

```bash
python ledger.py add "Canned Beans" --qty 12 --condition "sealed" --notes "Expiration 2050, good for morale"
python ledger.py add "Water Filter" --qty 1 --condition "used" --notes "Needs new cartridge soon"
```

*   `item_name`: The name of the item (required, enclose in quotes if it has spaces).
*   `--qty`: Quantity (default: 1).
*   `--condition`: Item's condition (default: "unknown").
*   `--notes`: Any additional notes.

#### ✏️ Update an Item

```bash
python ledger.py update "Canned Beans" --qty 10 --notes "Ate two, still good"
python ledger.py update "Water Filter" --condition "broken" --notes "Cartridge burst, useless now"
```

*   `item_name`: The name of the item to update (required).
*   `--qty`, `--condition`, `--notes`: Provide only the fields you wish to update. If a field is omitted, it remains unchanged.

#### 🗑️ Remove an Item

```bash
python ledger.py remove "Water Filter"
```

*   `item_name`: The name of the item to remove (required).

#### 📋 List All Items

```bash
python ledger.py list
```

This will print a formatted list of all items currently in your ledger.

#### 📁 Custom Ledger File

You can specify a different ledger file using the `--ledger-file` argument for any command:

```bash
python ledger.py --ledger-file my_special_stash.json add "Shiny Rock" --qty 1 --condition "glowing" --notes "Found near the old power plant"
python ledger.py --ledger-file my_special_stash.json list
```

## 🛠️ Development

### Project Structure

```
nightly-scavenger-supply-ledger/
├── README.md
├── src/
│   └── ledger.py
└── tests/
    └── test_ledger.py
```

### Running Tests

To run the tests, navigate to the `tests` directory and execute `pytest` (or `python -m unittest`):

```bash
cd utils/nightly-scavenger-supply-ledger/tests
python -m unittest test_ledger.py
```

The tests use `unittest.mock` to ensure they are deterministic and do not interact with the actual file system.
