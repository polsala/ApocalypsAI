# Apocalypse Resource Tracker

## 📦 Overview

Welcome, survivor! The 'Apocalypse Resource Tracker' is your trusty digital ledger for managing the precious supplies you've scavenged from the desolate wastes. Keep tabs on your canned goods, purified water, duct tape, and whatever else you find crucial for survival. Because even in the end times, organization is key!

This utility provides a simple command-line interface to add, update, remove, and list your inventory, persisting it to a local JSON file.

## ✨ Features

*   **Add Resources**: Easily add new items to your inventory with a specified quantity. If the item already exists, its quantity will be increased.
*   **Update Quantities**: Set the stock of an existing item to a specific new value.
*   **Remove Items**: Clear out items you no longer possess or need.
*   **List Inventory**: Get a clear overview of all your current resources, sorted alphabetically.
*   **Persistent Storage**: Your inventory is automatically saved and loaded from `inventory.json`.

## 🚀 Installation & Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/apocalypse-resource-tracker
    ```

2.  **Run the utility** (Python 3.8+ required):

    *   **Add an item**: Adds to the current quantity. If the item doesn't exist, it's created.
        ```bash
        python src/tracker.py add --name "Canned Beans" --quantity 10
        python src/tracker.py add --name "Purified Water" --quantity 5
        python src/tracker.py add --name "Canned Beans" --quantity 2 # Increases Canned Beans to 12
        ```

    *   **Update an item's quantity**: Sets the item to a specific new quantity. Does not create new items.
        ```bash
        python src/tracker.py update --name "Canned Beans" --quantity 8
        ```

    *   **Remove an item**: Deletes the item from your inventory.
        ```bash
        python src/tracker.py remove --name "Duct Tape"
        ```

    *   **List all items**: Displays your current inventory.
        ```bash
        python src/tracker.py list
        ```

## 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_tracker.py
```
