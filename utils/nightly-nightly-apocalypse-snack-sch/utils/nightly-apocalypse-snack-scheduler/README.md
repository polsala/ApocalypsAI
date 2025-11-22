# Nightly Apocalypse Snack Scheduler

## Overview

The `nightly-apocalypse-snack-scheduler` is a crucial utility for any discerning prepper or post-apocalyptic survivor. It helps you keep your emergency food and supply stash fresh and ready by tracking expiry dates and notifying you of items that need to be consumed or rotated soon.

No more discovering a forgotten can of 'Mystery Meat' from 2042 that expired in 2023! This tool ensures your vital sustenance remains viable.

## Features

*   **Expiry Tracking**: Monitors expiry dates for all listed items.
*   **Rotation Reminders**: Highlights items expiring within a configurable threshold (default: 30 days).
*   **Expired Item Alerts**: Clearly lists any items that have already passed their prime.
*   **Inventory Summary**: Provides an overview of your entire stash.

## Usage

1.  **Create your `snacks.yml` file**: Based on the `snacks.yml.example`, list your emergency supplies, their quantities, and their expiry dates.

    ```yaml
    # snacks.yml
    items:
      - name: 'Canned Beans (Kidney)'
        quantity: 12
        expiry_date: '2024-12-31'
      - name: 'MRE (Vegetarian Chili)'
        quantity: 5
        expiry_date: '2023-08-15'
      - name: 'Water Purification Tablets'
        quantity: 2
        expiry_date: '2025-06-01'
      - name: 'Emergency Rations Bar'
        quantity: 20
        expiry_date: '2024-03-20'
    ```

2.  **Run the scheduler**: Execute the script from the utility's directory.

    ```bash
    python3 src/snack_scheduler.py
    ```

    You can also specify a custom path to your `snacks.yml` and an expiry warning threshold (in days):

    ```bash
    python3 src/snack_scheduler.py --config /path/to/my_snacks.yml --warning-days 60
    ```

## Output Example

```
Apocalypse Snack Stash Report (Today: 2024-01-15)
=================================================

--- Expired Items (1) ---
- MRE (Vegetarian Chili) (5 units) - Expired 153 days (2023-08-15)

--- Expiring Soon (< 30 days) (1) ---
- Emergency Rations Bar (20 units) - Expires in 65 days (2024-03-20)

--- Healthy Stash (2) ---
- Canned Beans (Kidney) (12 units) - Expires in 351 days (2024-12-31)
- Water Purification Tablets (2 units) - Expires in 503 days (2025-06-01)

--- Inventory Summary ---
Total unique items: 4
Total units: 39
```

*(Note: The example output above is illustrative and will vary based on current date and your `snacks.yml` content.)*

## Development

To run tests:

```bash
python3 -m pytest tests/
```
