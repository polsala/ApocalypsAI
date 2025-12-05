# Wasteland Wanderer's Waypoint Weaver

A critical tool for any survivor navigating the treacherous post-apocalyptic landscape. The Waypoint Weaver helps you keep track of important locations – be it a hidden stash of purified water, a safe bunker, or a known mutant patrol route. Never get lost or forget a vital spot again!

## Features

*   **Add Waypoint**: Mark new locations with a name, description, and optional coordinates.
*   **List Waypoints**: View all your recorded waypoints at a glance.
*   **Remove Waypoint**: Delete outdated or no-longer-relevant waypoints.
*   **Persistent Storage**: All waypoints are saved to a `waypoints.json` file in the current directory, ensuring your crucial data survives reboots and power fluctuations.

## Installation

This utility is self-contained and requires Python 3.11+.

1.  Navigate to the `utils/wasteland-wanderer-waypoint-weaver/` directory.
2.  You can run it directly: `python src/waypoint_weaver.py`

## Usage

The `waypoint_weaver.py` script accepts several commands:

### Add a waypoint

```bash
python src/waypoint_weaver.py add "Old Gas Station" "Potential fuel source, watch for raiders." "34.0522,-118.2437"
```
(Coordinates are optional)
```bash
python src/waypoint_weaver.py add "Safehouse Alpha" "Abandoned library, good for shelter."
```

### List all waypoints

```bash
python src/waypoint_weaver.py list
```

### Remove a waypoint

```bash
python src/waypoint_weaver.py remove "Old Gas Station"
```

## Example Output

```
$ python src/waypoint_weaver.py add "The Glow" "Irradiated zone, avoid at all costs." "34.0,-118.0"
Waypoint 'The Glow' added.

$ python src/waypoint_weaver.py add "Water Cache" "Under the collapsed bridge."
Waypoint 'Water Cache' added.

$ python src/waypoint_weaver.py list
--- Waypoints ---
Name: The Glow
  Description: Irradiated zone, avoid at all costs.
  Coordinates: 34.0,-118.0
---
Name: Water Cache
  Description: Under the collapsed bridge.
  Coordinates: N/A
---
```
