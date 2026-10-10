# Nightly Apocalypse Day Counter

## Overview
A whimsical yet practical command‑line utility that calculates the number of days that have elapsed since the **Great Apocalypse** (fixed start date: 2023‑01‑01).  It can be used for fun project timelines, post‑apocalyptic logs, or simply to satisfy curiosity.

## Installation
```bash
# Clone the repository (or copy the utility folder) and run with Node.js 14+
node src/main.js --help
```

## Usage
```bash
# Calculate days since the apocalypse for today (default)
node src/main.js

# Specify a date (ISO format) to calculate for that day
node src/main.js --date 2023-02-15
```

### Options
- `--date <YYYY-MM-DD>` – The target date. If omitted, the current system date is used.
- `--help` – Show a short help message.

## Example Output
```
31 days since the Great Apocalypse (2023-01-01)
```

## Testing
Run the bundled tests with Node:
```bash
node tests/test_main.js
```
All tests should pass, confirming correct day calculations.
