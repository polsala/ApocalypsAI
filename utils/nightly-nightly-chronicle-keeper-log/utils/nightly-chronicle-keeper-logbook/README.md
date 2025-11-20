# Nightly Chronicle Keeper Logbook

## Overview
The Nightly Chronicle Keeper Logbook is a simple, yet essential command-line utility designed to help you record your thoughts, observations, and tasks with ease. In a world of chaos, keeping a clear record can be the difference between remembering a crucial discovery and losing it to the sands of time. Whether you're tracking resource caches, documenting strange anomalies, or simply jotting down your daily musings, this tool ensures your chronicles are timestamped and organized.

## Features
- **Timestamped Entries**: Every log entry is automatically prefixed with the current date and time.
- **Flexible Logging**: Log to a single, continuous `chronicle.md` file or opt for daily, date-specific log files (e.g., `2023-10-27_chronicle.md`).
- **Simple Interface**: Add entries with a single command.
- **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation
This utility is self-contained. Simply ensure you have Python 3.8+ installed.

## Usage

Log files will be created in the `logs/` subdirectory within the utility's root folder.

### Basic Logging (to `logs/chronicle.md`)
To add an entry to the default `logs/chronicle.md` file:
```bash
python src/logbook.py -m "Discovered a new supply cache near the old water tower."
```

### Daily Logging (to `logs/YYYY-MM-DD_chronicle.md`)
To add an entry to a daily log file:
```bash
python src/logbook.py -m "Repaired the solar panel array. Power levels stable." --daily
```

### Specifying a Custom Log File
You can also specify a different log file name. This file will still be placed in the `logs/` directory.
```bash
python src/logbook.py -m "Noted strange energy readings from Sector 7." -f "anomaly_report.md"
```

### Combining Options
```bash
python src/logbook.py -m "Found a working radio transmitter. Attempting to make contact." --daily -f "communications_log.md"
```
This will create/append to `logs/YYYY-MM-DD_communications_log.md`.

## Examples

**First entry:**
```bash
python src/logbook.py -m "Day 1 post-event. Supplies are low. Must scout west." --daily
```
`logs/2023-10-27_chronicle.md` (or current date) will contain:
```
### 2023-10-27 14:30:00
Day 1 post-event. Supplies are low. Must scout west.
```

**Second entry (same day, same file):**
```bash
python src/logbook.py -m "Encountered a pack of mutated squirrels. Managed to evade." --daily
```
`logs/2023-10-27_chronicle.md` will now contain:
```
### 2023-10-27 14:30:00
Day 1 post-event. Supplies are low. Must scout west.

### 2023-10-27 15:15:00
Encountered a pack of mutated squirrels. Managed to evade.
```

## Development
The `logbook.py` script is written in Python. Tests are located in `tests/test_logbook.py`.
To run tests:
```bash
python -m unittest tests/test_logbook.py
```
