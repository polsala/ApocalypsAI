# Nightly Resource Hoarder

A simple command-line utility for tracking your essential resources. Whether you're preparing for the next big event or just managing your pantry, the Resource Hoarder helps you keep tabs on what you have, how much, and where it is.

## Features

*   **Add Resources**: Easily add new items or update quantities of existing ones.
*   **Remove Resources**: Decrement quantities or remove items entirely.
*   **List Resources**: View your entire inventory at a glance.
*   **Persistent Storage**: Your inventory is saved to a local JSON file.

## Installation

This utility is self-contained and requires Python 3.8+. No external dependencies are needed.

1.  Navigate to the `utils/nightly-resource-hoarder/src` directory.
2.  Run the `tracker.py` script directly.

## Usage

```bash
python src/tracker.py --help
```

### Examples:

**Add 5 units of "Canned Beans"**:
```bash
python src/tracker.py add "Canned Beans" 5
```

**Add 2 units of "Water Filter"**:
```bash
python src/tracker.py add "Water Filter" 2
```

**Decrement "Canned Beans" by 1 (you ate one!)**:
```bash
python src/tracker.py remove "Canned Beans" 1
```

**List all resources**:
```bash
python src/tracker.py list
```

**Remove "Water Filter" entirely (if quantity becomes 0 or less)**:
```bash
python src/tracker.py remove "Water Filter" 2 # or more
```

The resource data is stored in `resources.json` in the same directory as `tracker.py`.
