# Nightly Rubble-Rouser Resource Tracker

## Overview

In the chaotic aftermath, every scrap counts! The Rubble-Rouser Resource Tracker is a simple command-line utility designed to help survivors keep tabs on their scavenged resources. It reads a plain text file containing your inventory, provides a summary of what you have, and highlights resources that are running low, ensuring you know what to prioritize on your next scavenging run.

## Features

*   **Inventory Tracking**: Easily log your resources in a simple text file.
*   **Resource Summary**: Get a quick overview of all your tracked items and their quantities.
*   **Low Resource Alerts**: Automatically identify resources below a configurable threshold.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

1.  **Prepare your resource file**: Create a plain text file (e.g., `resources.txt`) where each line represents a resource and its quantity, separated by a colon.

    Example `resources.txt`:
    ```
    Water: 15
    Canned Food: 8
    Batteries: 20
    Scrap Metal: 50
    Medical Supplies: 3
    Ammunition: 120
    Wood: 10
    ```

2.  **Run the tracker**:
    ```bash
    python src/tracker.py --file resources.txt --threshold 5
    ```

    *   `--file <path>`: Path to your resource inventory file (required).
    *   `--threshold <int>`: The quantity below which a resource is considered "low" (optional, default: 10).

## Example Output

```
--- Resource Inventory Summary ---
Water: 15 units
Canned Food: 8 units
Batteries: 20 units
Scrap Metal: 50 units
Medical Supplies: 3 units
Ammunition: 120 units
Wood: 10 units

--- Low Resources (below 5 units) ---
Medical Supplies: 3 units (CRITICAL!)
```

## Development

The utility is written in Python 3.11 and uses only standard library modules.
Tests are located in the `tests/` directory and can be run using `pytest` or `python -m unittest`.
