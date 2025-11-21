# Nightly Chronicle Keeper

## Overview

The `Nightly Chronicle Keeper` is a simple, self-contained command-line utility designed to help you log daily thoughts, events, or observations with automatic timestamps. It's perfect for keeping a personal journal, tracking project progress, or simply noting down important moments in the ongoing apocalypse. You can easily add new entries, list recent ones, or search through your entire chronicle.

## Features

*   **Timestamped Entries**: Every entry is automatically prepended with the current date and time.
*   **Easy Logging**: Quickly add new thoughts or events from your terminal.
*   **Browse History**: View your entire chronicle or just the most recent entries.
*   **Search Functionality**: Find specific entries using keywords (case-insensitive).
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is written in Python 3.11+ and requires no special installation steps or external packages. Simply place the `nightly-chronicle-keeper` folder in your desired location.

## Usage

Navigate to the `src` directory within the `nightly-chronicle-keeper` utility folder and run the `chronicle.py` script directly.

### Initialize the Chronicle (Optional, but recommended first run)

If the `.chronicle.log` file doesn't exist, it will be created automatically when you add an entry. You can also explicitly initialize it:

```bash
python3 chronicle.py init
```

### Add a New Entry

```bash
python3 chronicle.py add "Today, the sun rose again. A small victory."
```

### List Entries

List the 10 most recent entries (default):

```bash
python3 chronicle.py list
```

List the 5 most recent entries:

```bash
python3 chronicle.py list --count 5
```

List all entries:

```bash
python3 chronicle.py list --all
```

### Search Entries

Search for entries containing a specific keyword (case-insensitive):

```bash
python3 chronicle.py search "victory"
```

```bash
python3 chronicle.py search "sun"
```

## File Structure

```
nightly-chronicle-keeper/
├── README.md
├── src/
│   └── chronicle.py
└── tests/
    └── test_chronicle.py
```

Your chronicle entries will be stored in a file named `.chronicle.log` in the directory where you execute `chronicle.py`.
