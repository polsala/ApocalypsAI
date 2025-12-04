# Nightly Resource Tracker

## Overview

The `nightly-resource-tracker` is a simple, self-contained command-line utility designed to help you keep tabs on your vital resources in a post-apocalyptic (or just highly organized) world. Whether you're tracking water, food, power cells, or ammunition, this tool provides a quick way to log daily consumption and production, and view a summary of your current resource status.

It's perfect for those who believe that even in chaos, resource management is key to survival.

## Features

*   **Log Entries**: Easily record amounts of resources consumed or produced.
*   **Daily Summary**: Get a quick overview of your net resource changes for the current day.
*   **History View**: See all logged entries for a comprehensive look at your resource flow.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-resource-tracker/` directory.
2.  You can run the script directly:
    ```bash
    python src/tracker.py --help
    ```

## Usage

The `tracker.py` script supports the following commands:

### `add` - Log a resource transaction

Records an amount of a specific resource as either 'consumption' (default) or 'production'.

```bash
python src/tracker.py add <resource_name> <amount> [--type <consumption|production>]
```

*   `<resource_name>`: The name of the resource (e.g., `water`, `food_rations`, `power_cells`).
*   `<amount>`: The quantity of the resource. Use positive numbers. Consumption will be stored as negative, production as positive.
*   `--type`: Optional. Specify `consumption` (default) or `production`.

**Examples:**

```bash
python src/tracker.py add water 5 # Consumed 5 units of water
python src/tracker.py add food_rations 1 --type consumption # Consumed 1 food ration
python src/tracker.py add power_cells 2 --type production # Produced 2 power cells
```

### `summary` - View daily net changes

Displays the net change for all resources logged for the current day.

```bash
python src/tracker.py summary
```

### `history` - View all logged entries

Shows a chronological list of all resource transactions.

```bash
python src/tracker.py history
```

## Data Storage

Resource data is stored in a simple JSON file named `resources.json` within the `utils/nightly-resource-tracker/` directory. This file is automatically created if it doesn't exist.
