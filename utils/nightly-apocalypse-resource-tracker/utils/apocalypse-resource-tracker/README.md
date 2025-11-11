# Apocalypse Resource Tracker

A whimsical-yet-practical command-line utility to help you keep tabs on your essential pre-apocalyptic (or just emergency) supplies. Never run out of canned beans or fresh water again!

## Features

*   **Add/Update Resources**: Log items with quantity, expiry date, and notes.
*   **List Resources**: See all your tracked items at a glance.
*   **Expiry Alerts**: Get notified when resources are nearing their doom (expiry).
*   **Low Stock Warnings**: Identify items that need replenishment before the end times arrive.
*   **Persistent Storage**: Your precious resource data is saved to a local JSON file.

## Installation

This utility is self-contained and written in Python 3.11+.

1.  Navigate to the `utils/apocalypse-resource-tracker` directory.
2.  (Optional but recommended) Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  No external dependencies are required beyond standard Python libraries.

## Usage

Run the `tracker.py` script directly:

```bash
python3 src/tracker.py --help
```

### Examples:

*   **Add a new resource**:
    ```bash
    python3 src/tracker.py add --name "Canned Beans" --qty 12 --expiry "2025-12-31" --notes "Emergency protein"
    python3 src/tracker.py add --name "Water Bottles (1L)" --qty 24 --expiry "2030-01-01"
    ```
*   **Update an existing resource**:
    ```bash
    python3 src/tracker.py update --name "Canned Beans" --qty 10
    ```
*   **List all resources**:
    ```bash
    python3 src/tracker.py list
    ```
*   **Show expiring resources (within 60 days)**:
    ```bash
    python3 src/tracker.py expiring --days 60
    ```
*   **Show low-stock resources (below 5 units)**:
    ```bash
    python3 src/tracker.py low-stock --threshold 5
    ```
*   **Remove a resource**:
    ```bash
    python3 src/tracker.py remove --name "Canned Beans"
    ```

## Data Storage

Resource data is stored in `resources.json` within the utility's directory.

## Development

To run tests:

```bash
python3 -m unittest tests/test_tracker.py
```
