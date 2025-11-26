# Nightly Scavenger Logbook

## Overview
The Nightly Scavenger Logbook is a minimalist command-line utility designed for the discerning survivor. It allows you to quickly record your findings, their locations, and any pertinent notes in a timestamped, easy-to-read format. Keep track of that last can of beans, the location of a fresh water source, or that suspicious glowing rock.

## Features
*   **Timestamped Entries**: Every log entry is automatically stamped with the current date and time.
*   **Location Tracking**: Specify where you found or observed something.
*   **Detailed Notes**: Add a description of your finding.
*   **Simple Storage**: Logs are stored in a plain text file (`scavenger_log.txt`) for easy access and backup.

## Installation
This utility is self-contained. Simply navigate to the `src` directory and run it with Python 3.11+.

## Usage

### Add a new log entry
```bash
python src/logbook.py add --location "Old Supermart, Sector 7" --note "Found 3 cans of irradiated peaches. Edible?"
```

### View all log entries
```bash
python src/logbook.py view
```

### Example Output (view)
```
--- Scavenger Log ---
[2023-10-27 14:35:01] Location: Old Supermart, Sector 7 | Note: Found 3 cans of irradiated peaches. Edible?
[2023-10-27 14:40:15] Location: Abandoned Bunker 3 | Note: Discovered a working Geiger counter. Battery low.
---------------------
```
