# Nightly Temporal Supply Rotator

## Overview

In the desolate future, every scrap of sustenance counts. The `nightly-temporal-supply-rotator` is your trusty companion for managing perishable survival supplies. This whimsical Node.js CLI tool helps you track your inventory, reminds you which items are nearing their temporal decay (expiration), and ensures you rotate your stock efficiently to avoid waste.

Keep your larder organized and prevent precious resources from succumbing to the ravages of time!

## Features

*   **Add Supplies**: Easily add new items to your inventory with a name, quantity, and expiration date.
*   **List Inventory**: View all your supplies, sorted by their expiration date, with a clear indication of how many days remain until temporal decay.
*   **Use Supplies**: Mark items as used, reducing their quantity or removing them entirely if depleted.
*   **Temporal Reminders**: Get a quick overview of supplies that are nearing expiration within a specified threshold.

## Installation

This utility is a standalone Node.js script. No `npm install` is required beyond having Node.js installed on your system.

1.  Ensure you have Node.js (v14 or higher recommended) installed.
2.  Navigate to the `nightly-temporal-supply-rotator` directory.

## Usage

All commands are run using `node src/index.js <command> [arguments...]`.

### 1. Add a new supply

```bash
node src/index.js add <name> <quantity> <YYYY-MM-DD>
```

*   `<name>`: The name of the supply (e.g., "Canned Beans", "Water Purifier Tablets").
*   `<quantity>`: The numerical quantity of the item.
*   `<YYYY-MM-DD>`: The expiration date in `YYYY-MM-DD` format.

**Example:**

```bash
node src/index.js add "Emergency MRE" 10 2025-12-31
node src/index.js add "Medical Kit" 1 2024-06-15
```

### 2. List all supplies

```bash
node src/index.js list
```

This will display your entire inventory, sorted by expiration date, showing quantity and remaining days.

**Example Output:**

```
--- Temporal Larder Inventory ---
- Medical Kit (x1) - 2024-06-15 [Expires in 30 days (URGENT!)]
- Emergency MRE (x10) - 2025-12-31 [Expires in 500 days]
```

### 3. Use a supply

```bash
node src/index.js use <id> <quantity>
```

*   `<id>`: The unique ID of the supply (obtained from the `list` command).
*   `<quantity>`: The amount to use. If this depletes the item, it will be removed.

**Example:** (Assuming 'Medical Kit' has ID 1234567890)

```bash
node src/index.js use 1234567890 1
```

### 4. Get reminders for expiring supplies

```bash
node src/index.js remind [days_threshold]
```

*   `[days_threshold]`: (Optional) The number of days within which to consider an item "expiring soon". Defaults to 7 days.

**Example:**

```bash
node src/index.js remind 14  # Show items expiring in the next 14 days
node src/index.js remind     # Show items expiring in the next 7 days
```

## Data Storage

Your supply data is stored locally in a `supplies.json` file within the `src/` directory. This file is automatically created and managed by the utility.
