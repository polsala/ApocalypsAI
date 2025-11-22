# Nightly Rubble-Rouser Resource Tracker

## 📦 Overview

In the chaotic aftermath, every scrap counts! The Rubble-Rouser Resource Tracker is a simple, command-line utility designed to help you keep tabs on your precious scavenged goods, essential supplies, or even just your daily coffee bean count. It's a minimalist inventory system for the discerning survivor, ensuring you never lose track of that last can of irradiated peaches.

## ✨ Features

*   **Add Resources**: Increment the quantity of an existing resource or add a new one.
*   **Remove Resources**: Decrement the quantity of a resource.
*   **Set Resources**: Directly set the quantity of a resource, useful for corrections.
*   **List All Resources**: See your entire inventory at a glance.
*   **Persistent Storage**: Your inventory is saved to a local JSON file, so your hard-won gains are never lost.

## 🚀 Usage

Navigate to the `src` directory and run `tracker.py` with the desired command.

### Prerequisites

*   Python 3.6+

### Commands

*   **Add an item**:
    ```bash
    python src/tracker.py add "Canned Beans" 5
    ```
    Adds 5 units of "Canned Beans". If "Canned Beans" already exists, its quantity will be increased.

*   **Remove an item**:
    ```bash
    python src/tracker.py remove "Water Filters" 1
    ```
    Removes 1 unit of "Water Filters". If the quantity drops below zero, it will be set to zero.

*   **Set an item's quantity**:
    ```bash
    python src/tracker.py set "First Aid Kit" 2
    ```
    Sets the quantity of "First Aid Kit" to 2. This will overwrite any existing quantity.

*   **List all items**:
    ```bash
    python src/tracker.py list
    ```
    Displays your current inventory.

### Example Workflow

```bash
# Add some initial supplies
python src/tracker.py add "Scrap Metal" 10
python src/tracker.py add "Canned Goods" 3
python src/tracker.py add "Water Bottles" 6

# Check your inventory
python src/tracker.py list

# Use some supplies
python src/tracker.py remove "Canned Goods" 1

# Found more scrap!
python src/tracker.py add "Scrap Metal" 5

# Realized you miscounted water bottles
python src/tracker.py set "Water Bottles" 5

# Final check
python src/tracker.py list
```

## 🛠️ Development

The tracker stores its data in `resources.json` within the `src/` directory.
