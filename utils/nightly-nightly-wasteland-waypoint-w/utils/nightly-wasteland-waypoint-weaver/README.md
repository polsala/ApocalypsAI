# Nightly Wasteland Waypoint Weaver

## Description
In the desolate expanse of the post-apocalypse, reliable navigation and threat assessment are paramount. The `Nightly Wasteland Waypoint Weaver` is a simple, yet robust, command-line utility designed to help survivors track and manage critical locations (waypoints).

Whether you're mapping out a new scavenging route, marking a safe haven, or pinpointing a 'Death Trap' infested with irradiated horrors, this tool keeps your vital intel organized.

## Features
- **Add Waypoints**: Record new locations with names, coordinates, descriptions, and a danger level.
- **List Waypoints**: View all your recorded waypoints in a clear, tabular format.
- **Remove Waypoints**: Delete outdated or irrelevant waypoints.
- **Persistent Storage**: Waypoints are automatically saved to and loaded from a `waypoints.json` file.

## Installation
This utility is self-contained and requires Python 3.8+.

1.  Navigate to the `utils/nightly-wasteland-waypoint-weaver/` directory.
2.  You can run it directly using `python src/waypoint_weaver.py`.

## Usage
All commands are executed via the `waypoint_weaver.py` script.

### Add a Waypoint
```bash
python src/waypoint_weaver.py add --name "Old Gas Station" --lat 34.0522 --lon -118.2437 --desc "Potential fuel, watch for raiders." --danger "Caution"
python src/waypoint_weaver.py add --name "Vault 76 Entrance" --lat 38.9072 --lon -77.0369 --desc "Rumored safe zone, but heavily guarded." --danger "Dangerous"
```

**Arguments for `add`:**
- `--name <string>`: Unique name for the waypoint.
- `--lat <float>`: Latitude coordinate.
- `--lon <float>`: Longitude coordinate.
- `--desc <string>`: A brief description of the location.
- `--danger <string>`: Danger level (e.g., "Safe", "Caution", "Dangerous", "Death Trap").

### List All Waypoints
```bash
python src/waypoint_weaver.py list
```

### Remove a Waypoint
```bash
python src/waypoint_weaver.py remove --name "Old Gas Station"
```

**Arguments for `remove`:**
- `--name <string>`: The name of the waypoint to remove.

## Example `waypoints.json` structure
```json
[
  {
    "name": "Old Gas Station",
    "lat": 34.0522,
    "lon": -118.2437,
    "description": "Potential fuel, watch for raiders.",
    "danger_level": "Caution"
  },
  {
    "name": "Vault 76 Entrance",
    "lat": 38.9072,
    "lon": -77.0369,
    "description": "Rumored safe zone, but heavily guarded.",
    "danger_level": "Dangerous"
  }
]
```
