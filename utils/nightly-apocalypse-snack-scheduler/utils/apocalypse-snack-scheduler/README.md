# Apocalypse Snack Scheduler

## Overview

In these uncertain times, ensuring your 'apocalypse-ready' snack and supply stash is fresh and up-to-date is paramount. The `apocalypse-snack-scheduler` is a simple, whimsical utility designed to help you keep track of when your vital provisions need checking, rotating, or replenishing.

It reads a configuration file detailing your supplies, their last check dates, and how often they should be reviewed. Based on the current date, it will tell you which items are due for inspection.

## Features

*   **Configurable Supplies**: Define your own list of emergency snacks and supplies.
*   **Scheduled Reminders**: Calculates the next check date for each item.
*   **Clear Reporting**: Outputs a list of items that are due for checking today or are overdue.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

## Usage

1.  **Create your `snacks.json` file**: In the `src/` directory (or the directory where you run `snack_scheduler.py` from), create a JSON file named `snacks.json`. This file should contain an array of objects, each representing a supply item.

    Example `snacks.json`:
    ```json
    [
        {
            "name": "Canned Beans (Emergency Stock)",
            "last_checked": "2023-01-15",
            "check_frequency_days": 180
        },
        {
            "name": "MREs (Main Ration Pack)",
            "last_checked": "2023-06-01",
            "check_frequency_days": 365
        },
        {
            "name": "Water Purification Tablets",
            "last_checked": "2024-03-10",
            "check_frequency_days": 90
        },
        {
            "name": "Survival Biscuits",
            "last_checked": "2024-07-01",
            "check_frequency_days": 14
        }
    ]
    ```

    *   `name`: A descriptive name for your supply item.
    *   `last_checked`: The date (YYYY-MM-DD) when you last checked this item.
    *   `check_frequency_days`: How often (in days) this item should be checked.

2.  **Run the scheduler**:

    Navigate to the `utils/apocalypse-snack-scheduler/` directory and run:

    ```bash
    python3 src/snack_scheduler.py
    ```

## Example Output

```
Apocalypse Snack Scheduler Report (Today: 2024-07-15)
---------------------------------------------------

Items due for checking:

- Canned Beans (Emergency Stock) - Overdue since 2023-07-14 (Last checked: 2023-01-15)
- Survival Biscuits - Due today since 2024-07-15 (Last checked: 2024-07-01)

All other items are up-to-date. Stay vigilant!
```

## Development

To run tests:

Navigate to the `utils/apocalypse-snack-scheduler/` directory and run:

```bash
python3 -m unittest tests/test_snack_scheduler.py
```
