# Nightly Chronicle Keeper

A simple, whimsical command-line utility to record your daily observations, progress, or "apocalyptic" events in a local, timestamped chronicle. Keep track of your journey through the digital wasteland!

## Features

*   **Log Entries**: Quickly add new timestamped entries to your personal chronicle.
*   **View Chronicle**: Display all recorded entries.
*   **Search Entries**: Find specific entries using keywords.
*   **Self-contained**: No external dependencies, just pure Python.

## Installation

This utility is self-contained. Simply place the `nightly-chronicle-keeper` folder in your desired location.

## Usage

Navigate to the `src` directory within `nightly-chronicle-keeper` and run `chronicle_keeper.py` with the desired command.

```bash
# Initialize the chronicle file (if it doesn't exist)
python chronicle_keeper.py init

# Add a new entry
python chronicle_keeper.py add "Discovered a new bug in the build system. The robots are restless."

# View the entire chronicle
python chronicle_keeper.py view

# Search for entries containing a specific keyword
python chronicle_keeper.py search "robots"
```

### Commands

*   `init`: Creates the `chronicle.log` file if it doesn't exist.
*   `add <message>`: Appends a new timestamped entry with `<message>` to `chronicle.log`.
*   `view`: Prints the entire content of `chronicle.log` to the console.
*   `search <keyword>`: Prints all entries from `chronicle.log` that contain `<keyword>`.

## Chronicle File Location

By default, the `chronicle.log` file will be created in the same directory as `chronicle_keeper.py`.
