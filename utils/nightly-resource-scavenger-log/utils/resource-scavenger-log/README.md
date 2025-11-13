# Resource Scavenger Log

## Overview

The `resource-scavenger-log` is a vital tool for any survivor navigating the desolate landscapes of the post-apocalypse. It's a simple command-line utility designed to help you meticulously log every precious resource you scavenge, ensuring you never lose track of your vital supplies.

Whether it's a cache of canned goods, a stash of purified water, or a rare piece of pre-collapse tech, this log will keep your inventory organized and ready for the next challenge.

## Features

*   **Add Resources**: Quickly log new discoveries with details like resource name, quantity, unit, location, and the date of discovery.
*   **List Resources**: View all your logged resources in an easy-to-read format.
*   **Generate Report**: Get a summary of your resources, showing total quantities per resource type.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

## Usage

Navigate to the `src` directory within the `resource-scavenger-log` utility folder.

### Add a new resource

```bash
python scavenger_log.py add \
  --resource "Canned Peaches" \
  --quantity 5 \
  --unit "cans" \
  --location "Abandoned Grocery Store - Aisle 7" \
  --date "2024-07-20"
```

*   `--resource`: The name of the resource (e.g., "Water Bottle", "Scrap Metal").
*   `--quantity`: The amount found (integer).
*   `--unit`: The unit of measurement (e.g., "bottles", "kg", "pieces").
*   `--location`: Where the resource was found (e.g., "Old Bunker Cache", "Rubble Pile Sector 4").
*   `--date`: (Optional) The date of discovery in YYYY-MM-DD format. Defaults to today's date.

### List all logged resources

```bash
python scavenger_log.py list
```

### Generate a summary report

```bash
python scavenger_log.py report
```

## Data Storage

Resource data is stored in a simple JSON file named `resources.json` within the `src` directory. This makes it easy to inspect or even manually edit if needed (though caution is advised!).
