# Nightly Scavenger's Stash Locator

A command-line utility to help survivors keep track of important locations or "stashes" in the wasteland. Whether it's a hidden cache of supplies, a safe house, or a dangerous anomaly, this tool helps you log and retrieve your valuable finds.

## Features

*   **Add Stash**: Log a new location with a name, description, and coordinates.
*   **List Stashes**: View all your recorded stashes.
*   **Find Stash**: Quickly locate a specific stash by its name.
*   **Remove Stash**: Delete a stash entry when it's no longer relevant (or has been scavenged dry).
*   **Persistent Storage**: Stashes are saved to a `stashes.json` file, so your data persists between sessions.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

```bash
# Navigate to the utility's directory
cd utils/nightly-scavengers-stash-locator/src
```

## Usage

All commands are run via `python stash_locator.py <command> [arguments]`.

### Add a Stash

```bash
python stash_locator.py add "Old World Library" "Contains pre-collapse knowledge, possibly dusty." "X:45.12,Y:-123.45"
# Output: Stash 'Old World Library' added.
```

### List All Stashes

```bash
python stash_locator.py list
# Output:
# --- Your Stashes ---
# Name: Old World Library
#   Description: Contains pre-collapse knowledge, possibly dusty.
#   Coordinates: X:45.12,Y:-123.45
# --------------------
# Name: Abandoned Bunker
#   Description: Rumored to hold advanced tech, but heavily guarded.
#   Coordinates: X:10.00,Y:20.00
# --------------------
```

### Find a Stash

```bash
python stash_locator.py find "Abandoned Bunker"
# Output:
# --- Stash Found: Abandoned Bunker ---
#   Description: Rumored to hold advanced tech, but heavily guarded.
#   Coordinates: X:10.00,Y:20.00
```

### Remove a Stash

```bash
python stash_locator.py remove "Old World Library"
# Output: Stash 'Old World Library' removed.
```

### Using a Custom Data File

You can specify a different JSON file to store your stashes using the `--data-file` argument:

```bash
python stash_locator.py --data-file my_special_stashes.json add "Secret Hideout" "Only for the bravest." "X:999,Y:999"
```

## Development

To run tests:

```bash
# Navigate to the utility's directory
cd utils/nightly-scavengers-stash-locator/tests
python -m unittest test_stash_locator.py
```
