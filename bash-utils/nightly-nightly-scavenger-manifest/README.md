# Nightly Scavenger's Manifest Manager (`nightly-scavenger-manifest`)

A whimsical-yet-useful bash utility for managing your precious scavenged goods in the post-apocalyptic wasteland. Keep track of your inventory, categorize items, and quickly check your stock with this simple command-line tool.

## Usage

The utility operates on a `manifest.txt` file in the current directory. Each line in `manifest.txt` should follow the format: `CATEGORY: ITEM_NAME: QUANTITY`.

```
FOOD: Canned Beans: 5
WEAPON: Rusty Pipe: 1
TOOL: Wrench: 2
FOOD: Purified Water: 10
WEAPON: Makeshift Bow: 1
```

### Commands

*   **`./scavenger-manifest.sh init`**
    Initializes an empty `manifest.txt` file if it doesn't exist.

*   **`./scavenger-manifest.sh add <CATEGORY> <ITEM_NAME> <QUANTITY>`**
    Adds a new item or updates the quantity of an existing item in the manifest. If the item already exists (same category and item name), its quantity will be incremented. `QUANTITY` must be a positive integer.
    Example: `./scavenger-manifest.sh add FOOD "Canned Beans" 3`

*   **`./scavenger-manifest.sh list [CATEGORY]`**
    Lists all items in the manifest. If a `CATEGORY` is provided, it will only list items belonging to that category (case-insensitive).
    Example: `./scavenger-manifest.sh list`
    Example: `./scavenger-manifest.sh list FOOD`

*   **`./scavenger-manifest.sh summary`**
    Provides a summarized view of all items, showing the total quantity for each unique item name across all categories. The output is sorted alphabetically by item name.
    Example: `./scavenger-manifest.sh summary`

*   **`./scavenger-manifest.sh check <ITEM_NAME>`**
    Checks if a specific item exists in the manifest (case-insensitive). Returns an exit code of 0 if found, 1 if not found.
    Example: `./scavenger-manifest.sh check "Wrench"`

## Installation

Simply place `scavenger-manifest.sh` in your desired directory and make it executable:

```bash
chmod +x scavenger-manifest.sh
```

## Examples

```bash
# Initialize the manifest
./scavenger-manifest.sh init

# Add some items
./scavenger-manifest.sh add FOOD "Canned Beans" 5
./scavenger-manifest.sh add WEAPON "Rusty Pipe" 1
./scavenger-manifest.sh add TOOL "Wrench" 2
./scavenger-manifest.sh add FOOD "Purified Water" 10
./scavenger-manifest.sh add FOOD "Canned Beans" 2 # Adds to existing quantity

# List all items
./scavenger-manifest.sh list

# List food items
./scavenger-manifest.sh list FOOD

# Get a summary of all items
./scavenger-manifest.sh summary

# Check for an item
./scavenger-manifest.sh check "Wrench"
echo $? # Should be 0

./scavenger-manifest.sh check "Medical Kit"
echo $? # Should be 1
```
