# Nightly Scavenger Scrutiny Log

A robust, yet delightfully simple, command-line utility for the discerning post-apocalyptic scavenger. Keep meticulous records of your findings, categorize your loot, and never again wonder where you stashed that last can of irradiated beans.

## Features

*   **Log Findings**: Easily add new items with details like name, category, condition, and location.
*   **Timestamped Entries**: Every log entry is automatically timestamped for historical context.
*   **List All Loot**: View a comprehensive list of all your recorded treasures.
*   **Search & Filter**: Quickly find specific items by name, category, or location.
*   **Persistent Storage**: All logs are saved to a local JSON file, surviving even the most unexpected data wipes (unless the server itself is wiped, of course).

## Installation

This utility is self-contained and requires Python 3.8+ (or compatible).

1.  Navigate to the `utils/nightly-scavenger-scrutiny-log/` directory.
2.  Run the script directly.

## Usage

The `scrutiny_log.py` script accepts several commands: `add`, `list`, and `search`.

### `add` - Log a new finding

```bash
python src/scrutiny_log.py add --item "Irradiated Beans" --category "Food" --condition "Good" --location "Old Supermart Shelf 3"
python src/scrutiny_log.py add --item "Rusty Wrench" --category "Tool" --condition "Damaged" --location "Abandoned Garage"
```

*   `--item`: The name of the item found (required).
*   `--category`: The category of the item (e.g., Food, Tool, Weapon, Component). Defaults to "Misc".
*   `--condition`: The condition of the item (e.g., Good, Damaged, Broken, Pristine). Defaults to "Unknown".
*   `--location`: Where the item was found or stored. Defaults to "Unspecified".

### `list` - Display all logged findings

```bash
python src/scrutiny_log.py list
```

### `search` - Find specific items

```bash
python src/scrutiny_log.py search --query "beans"
python src/scrutiny_log.py search --category "Tool"
python src/scrutiny_log.py search --location "Supermart"
```

*   `--query`: A keyword to search for in item names.
*   `--category`: Filter by item category.
*   `--location`: Filter by item location.

## Example Output

```
--- Scavenger's Scrutiny Log ---
[2023-10-27 10:00:00] Item: Irradiated Beans, Category: Food, Condition: Good, Location: Old Supermart Shelf 3
[2023-10-27 10:05:30] Item: Rusty Wrench, Category: Tool, Condition: Damaged, Location: Abandoned Garage
```
