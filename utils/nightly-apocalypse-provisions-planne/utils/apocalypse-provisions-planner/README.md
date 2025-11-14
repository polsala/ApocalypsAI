# Apocalypse Provisions Planner

A whimsical utility to help you manage your essential "apocalypse" provisions. Define your desired stock levels, track your current inventory, and generate a shopping list for items running low. Never run out of critical supplies (like artisanal jerky or emergency glitter) again!

## Usage

1.  **Configure your provisions:** Create a `provisions.json` file in the utility's root directory (or specify its path via `--provisions-file`). This file defines the items you want to keep in stock and their target quantities.

    Example `provisions.json`:
    ```json
    {
        "emergency glitter": {"target": 10, "unit": "jars"},
        "canned beans": {"target": 24, "unit": "cans"},
        "artisanal jerky": {"target": 5, "unit": "packs"},
        "water purification tablets": {"target": 100, "unit": "tablets"}
    }
    ```

2.  **Track your inventory:** Create an `inventory.json` file (or specify its path via `--inventory-file`). This file tracks your current stock levels.

    Example `inventory.json`:
    ```json
    {
        "emergency glitter": 7,
        "canned beans": 20,
        "artisanal jerky": 3,
        "water purification tablets": 95
    }
    ```

3.  **Run the planner:**

    *   **Check inventory and generate shopping list:**
        ```bash
        python src/planner.py check
        ```
        This will print a list of items you need to acquire to reach your target stock levels.

    *   **Consume items from inventory:**
        ```bash
        python src/planner.py consume "emergency glitter" 2
        ```
        This command reduces the quantity of "emergency glitter" by 2 in your `inventory.json`.

    *   **Add items to inventory (after shopping):**
        ```bash
        python src/planner.py add "canned beans" 4
        ```
        This command increases the quantity of "canned beans" by 4 in your `inventory.json`.

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `utils/apocalypse-provisions-planner` directory.
2.  Create your `provisions.json` and `inventory.json` files as described above.
3.  Run the commands as shown in the Usage section.
