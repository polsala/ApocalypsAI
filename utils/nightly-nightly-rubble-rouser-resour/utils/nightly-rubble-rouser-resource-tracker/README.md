# Nightly Rubble-Rouser Resource Tracker

## Overview

In the desolate aftermath, every scrap counts. The Nightly Rubble-Rouser Resource Tracker is a simple command-line utility designed to help survivors keep tabs on their scavenged goods across various stash locations. Whether it's a cache of canned goods in an abandoned supermarket or a pile of scrap metal near a collapsed bridge, this tool ensures you always know what you have and where to find it.

## Features

*   **Location-based Tracking**: Organize resources by their physical stash location.
*   **Quantity Management**: Add, update, and view quantities of various items.
*   **Simple Interface**: Easy-to-use command-line arguments for quick inventory checks.
*   **Persistent Storage**: Saves your inventory data to a JSON file.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

## Usage

```bash
python src/tracker.py --help
```

### Examples

1.  **Initialize/View all resources (if `resources.json` doesn't exist, it will be created empty):**
    ```bash
    python src/tracker.py list
    ```

2.  **Add a new resource to a location:**
    ```bash
    python src/tracker.py add --location "Old Gas Station" --item "Fuel Can" --quantity 5
    ```

3.  **Update an existing resource's quantity:**
    ```bash
    python src/tracker.py update --location "Old Gas Station" --item "Fuel Can" --quantity 7
    ```

4.  **List resources at a specific location:**
    ```bash
    python src/tracker.py list --location "Old Gas Station"
    ```

5.  **List a specific item across all locations:**
    ```bash
    python src/tracker.py list --item "Water Filter"
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_tracker.py
```
