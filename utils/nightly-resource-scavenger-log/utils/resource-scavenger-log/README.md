# Resource Scavenger Log

A simple command-line utility to help survivors track their precious finds in the desolate wastes. Log items, quantities, and locations to keep your inventory organized and your survival chances high!

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/resource-scavenger-log/` directory.
2.  You can run the script directly:
    ```bash
    python3 src/scavenger_log.py --help
    ```

## Usage

### Add a new resource entry

To log a new discovery, use the `add` command:

```bash
python3 src/scavenger_log.py add <item_name> <quantity> <location>
```

-   `<item_name>`: The name of the resource (e.g., "Canned Beans", "Purified Water", "Scrap Metal").
-   `<quantity>`: The amount found (e.g., "5", "1.5L", "20kg").
-   `<location>`: Where you found it (e.g., "Old Supermart", "Collapsed Bridge", "Sector 7 Outpost").

**Example:**

```bash
python3 src/scavenger_log.py add "Canned Peaches" 3 "Abandoned Farmhouse"
python3 src/scavenger_log.py add "Rusty Pipe" 1 "Sewer Entrance"
```

### List all logged resources

To view all your logged resources, use the `list` command:

```bash
python3 src/scavenger_log.py list
```

This will display a formatted table of all your discoveries, including the timestamp of when they were logged.

## Data Storage

All resource logs are stored in a CSV file named `scavenger_log.csv` in the directory where the script is executed. This makes it easy to manage and even manually inspect or edit your log if needed.

## Development

To run tests:

```bash
python3 -m unittest tests/test_scavenger_log.py
```
