# Nightly Wasteland Wayfinder

A crucial tool for any survivor navigating the treacherous post-apocalyptic landscape. The Wasteland Wayfinder allows you to meticulously log and retrieve information about important locations – be they safe zones, resource caches, or areas teeming with mutated horrors. Never get lost or forget a critical landmark again!

## Features

*   **Add Landmarks**: Log new locations with a name, coordinates, type (e.g., "safe_zone", "resource_cache", "danger_area"), and an optional description.
*   **List All**: View a comprehensive list of all recorded landmarks.
*   **Find Specifics**: Search for landmarks by name or type.
*   **Remove Entries**: Delete outdated or irrelevant location data.

## Installation

This utility is self-contained and requires Python 3.11+.

```bash
# No installation needed beyond cloning the repository.
# Navigate to the utility's directory:
cd utils/nightly-wasteland-wayfinder/src
```

## Usage

All commands are executed via `python wayfinder.py <command> [arguments]`.

### Add a new landmark

```bash
python wayfinder.py add "Old World Bunker" "34.0522,-118.2437" "safe_zone" "Well-stocked, but entrance is tricky."
python wayfinder.py add "Scrap Metal Pile" "34.0000,-118.0000" "resource_cache"
python wayfinder.py add "Mutant Den" "34.1234,-118.5678" "danger_area" "Beware of glowing eyes."
```

### List all landmarks

```bash
python wayfinder.py list
```

### Find landmarks

Search by name (partial match) or type:

```bash
python wayfinder.py find "bunker"
python wayfinder.py find "resource_cache"
```

### Remove a landmark

```bash
python wayfinder.py remove "Scrap Metal Pile"
```

## Data Storage

Landmark data is stored in a `landmarks.json` file within the `src/` directory. This file is automatically created and managed by the utility.
