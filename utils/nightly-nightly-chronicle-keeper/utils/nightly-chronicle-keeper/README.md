# Nightly Chronicle Keeper

A simple, yet essential, command-line utility for documenting your daily journey through the remnants of civilization. Whether you're tracking resource caches, noting strange occurrences, or simply journaling your thoughts, the Chronicle Keeper ensures your entries are timestamped and organized.

## Features

*   **Timestamped Entries**: Every log entry is automatically prefixed with the current date and time.
*   **Daily Log Files**: Entries are organized into separate files for each day (`YYYY-MM-DD.log`) within a dedicated `chronicles/` directory.
*   **Simple CLI**: Quick and easy to use from your terminal.

## Usage

To add an entry to your chronicle:

```bash
python src/chronicle_keeper.py "Found a rusty can of beans near the old gas station. Tasted... metallic."
```

Or, for a more concise entry:

```bash
python src/chronicle_keeper.py "Repaired the solar panel array. Power at 70%."
```

The utility will create a `chronicles/` directory in the current working directory (if it doesn't exist) and append your message to the appropriate daily log file.

## Example Log File (`chronicles/2023-10-27.log`)

```
[2023-10-27 14:35:01] Found a rusty can of beans near the old gas station. Tasted... metallic.
[2023-10-27 15:10:45] Repaired the solar panel array. Power at 70%.
```

## Installation

This utility is self-contained and requires no special installation beyond a Python 3.11+ environment. Simply place the `nightly-chronicle-keeper` folder in your desired location.
