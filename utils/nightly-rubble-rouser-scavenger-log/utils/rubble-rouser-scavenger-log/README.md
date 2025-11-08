# Rubble-Rouser's Resource Scavenger Log

## Overview
In the desolate wastes, every scrap counts! The `rubble-rouser-scavenger-log` is a simple command-line utility designed for the discerning survivor to meticulously record their scavenged treasures. Keep track of what you found, where you found it, and any crucial notes about its condition or potential uses. Never lose track of that pristine can of beans or that suspiciously glowing wrench again!

## Features
- **Add Entry**: Log new scavenged items with details.
- **View Log**: Display all recorded entries.
- **Search Log**: Find specific items by keyword.

## Installation
This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

```bash
# Navigate to the utility directory
cd utils/rubble-rouser-scavenger-log/src
```

## Usage

The log data is stored in `scavenger_log.json` within the `src/` directory.

### Add a new entry
```bash
python scavenger_log.py add --item "Rusty Crowbar" --location "Old Supermart Basement" --quantity 1 --notes "Good for prying, might need sharpening."
python scavenger_log.py add --item "Canned Peaches" --location "Abandoned Bunker 7" --quantity 3 --notes "Expiration date unclear, but smells okay."
```

### View all entries
```bash
python scavenger_log.py view
```

### Search for entries
```bash
python scavenger_log.py search --keyword "crowbar"
python scavenger_log.py search --keyword "canned"
```

## Development & Testing
To run the tests, navigate to the `tests/` directory and execute:
```bash
python -m unittest test_scavenger_log.py
```
