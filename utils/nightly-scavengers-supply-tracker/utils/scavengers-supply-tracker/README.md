# Scavenger's Supply Tracker

## 🗺️ Keep Your Loot Organized in the Wastes!

In the desolate future, every scrap counts! The Scavenger's Supply Tracker is your trusty digital companion for cataloging the precious resources you unearth across the ravaged landscape. Whether it's a cache of canned goods in the 'Old Supermarket' or a stash of rare components in the 'Abandoned Research Lab', this tool ensures you never lose track of your vital supplies.

### ✨ Features

*   **Location-based Tracking**: Organize supplies by the specific zones or buildings where you found them.
*   **Quantity Management**: Easily add, update, or remove quantities of items.
*   **Simple CLI**: A straightforward command-line interface for quick inventory updates.
*   **Persistent Storage**: Your precious data is saved locally in a `supplies.json` file.

### 🚀 Installation

This utility is written in Python 3.11 and requires no external dependencies beyond the standard library. Simply place the `scavengers-supply-tracker` folder in your desired location.

### 🛠️ Usage

Navigate into the `src` directory of the utility:

```bash
cd utils/scavengers-supply-tracker/src
```

Then run the `tracker.py` script with your desired commands.

#### ➕ Add Supplies

Add new items or increase the quantity of existing ones in a specific location.

```bash
python tracker.py add "Old Supermarket" "Canned Beans" 5
python tracker.py add "Abandoned Farm" "Purified Water" 10
python tracker.py add "Old Supermarket" "Canned Beans" 3 # Adds 3 more beans
```

#### 📜 List Supplies

View all your tracked supplies, or filter by a specific location.

```bash
python tracker.py list
# Output:
# --- Abandoned Farm ---
#   - Purified Water: 10
# --- Old Supermarket ---
#   - Canned Beans: 8

python tracker.py list --location "Old Supermarket"
# Output:
# --- Old Supermarket ---
#   - Canned Beans: 8
```

#### ➖ Remove Supplies

Remove a specific quantity of an item, or remove all of it if no quantity is specified.

```bash
python tracker.py remove "Old Supermarket" "Canned Beans" --quantity 2 # Removes 2 beans
python tracker.py remove "Abandoned Farm" "Purified Water" # Removes all purified water
```

### 💾 Data Storage

Your supply data is stored in a `supplies.json` file located in the same `src` directory as `tracker.py`. This file is automatically created and managed by the utility.

Example `supplies.json` content:

```json
{
    "locations": {
        "Old Supermarket": [
            {
                "item": "Canned Beans",
                "quantity": 6
            }
        ],
        "Abandoned Farm": []
    }
}
```

Happy scavenging, survivor!
