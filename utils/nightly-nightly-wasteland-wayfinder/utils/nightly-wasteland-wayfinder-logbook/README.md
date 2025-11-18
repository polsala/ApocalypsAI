# Wasteland Wayfinder Logbook

## Description
In the desolate expanse of the post-apocalyptic world, reliable navigation and information logging are paramount. The `Wasteland Wayfinder Logbook` is a simple, command-line utility designed to help survivors track their journeys, mark points of interest (POIs), and record potential hazards. It stores entries in a human-readable text file, making it easy to review and share vital intelligence.

## Features
- **Log Entries**: Record new routes, POIs, hazards, or general notes with a timestamp, type, location, and description.
- **List All Entries**: View a chronological list of all logged information.
- **Search Entries**: Filter entries by keywords to quickly find specific information.

## Usage

### Prerequisites
- Python 3.6+

### Installation
This utility is self-contained. Simply navigate to the `src` directory and run the `wayfinder.py` script.

### Commands

#### 1. Add a new entry
```bash
python src/wayfinder.py add --type <TYPE> --location "<LOCATION>" --description "<DESCRIPTION>"
```
- `<TYPE>`: `ROUTE`, `POI` (Point of Interest), `HAZARD`, or `NOTE`.
- `<LOCATION>`: A descriptive location (e.g., "Old Gas Station (34.5, -118.2)", "Ruined Bridge over River Styx").
- `<DESCRIPTION>`: Detailed notes about the entry.

**Example:**
```bash
python src/wayfinder.py add --type POI --location "Abandoned Supermarket (N34.05, W118.25)" --description "Found canned goods, mostly expired. Some usable tools in back room."
python src/wayfinder.py add --type ROUTE --location "From Safehouse Alpha to Water Source Beta" --description "Followed old highway 101, mostly clear. Watch for mutated wildlife near mile marker 5."
python src/wayfinder.py add --type HAZARD --location "Collapsed Tunnel Entrance (N34.10, W118.30)" --description "Blocked by rubble, unstable. Seek alternative route through hills."
```

#### 2. List all entries
```bash
python src/wayfinder.py list
```

#### 3. Search entries
```bash
python src/wayfinder.py search --query "generator"
```
- `--query`: A keyword or phrase to search for within the entry descriptions or locations.

## Log File Format
Entries are stored in `wayfinder_log.txt` (located in the `src` directory) in the following pipe-delimited format:
`TIMESTAMP | TYPE | LOCATION | DESCRIPTION`

Example:
```
2024-10-27 14:30:00 | POI | Old Gas Station (34.5, -118.2) | Found a working generator, low on fuel. Marked on map.
2024-10-27 15:00:00 | ROUTE | From Safehouse Alpha to Water Source Beta | Followed old highway 101, mostly clear. Watch for mutated wildlife near mile marker 5.
```
