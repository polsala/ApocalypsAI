# Nightly Chronicle Keeper Logbook

A simple command-line utility for creating and managing timestamped log entries. Whether you're tracking the spread of the fungal bloom, noting down scavenging routes, or just journaling your thoughts on the end of days, the Chronicle Keeper ensures your records are safe and sound.

## Features

*   **Timestamped Entries**: Every log entry is automatically stamped with the current date and time.
*   **Easy Logging**: Quickly add new entries from the command line.
*   **Searchable History**: Find specific entries using keywords.
*   **List All Entries**: View your entire chronicle.
*   **Self-Contained**: Stores logs in a simple text file within its directory.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-chronicle-keeper-logbook/` directory.
2.  Run the `logbook.py` script directly.

## Usage

All commands are run via `python src/logbook.py <command> [arguments]`.

### Add a new entry

```bash
python src/logbook.py add "Found a pristine can of beans near Sector 7."
```

### List all entries

```bash
python src/logbook.py list
```

### Search for entries

```bash
python src/logbook.py search "beans"
```

### Clear all entries (use with caution!)

```bash
python src/logbook.py clear
```
You will be prompted for confirmation before clearing.
