# Rubble-Rouser's Resource Tracker

## Overview

In the grim future of the ApocalypsAI, every scrap counts. The `Rubble-Rouser's Resource Tracker` is a vital Python utility designed to help survivors manage their dwindling supplies. Whether it's irradiated rations, purified rainwater, salvaged power cells, or precious bullets, this tool provides a clear overview of your current stock and estimates how long each resource will last based on your daily consumption.

Stay ahead of the inevitable, plan your scavenging runs, and ensure your survival for another day (or week, if you're lucky!).

## Features

*   **Resource Management**: Add, consume, and check levels of various resources.
*   **Survival Estimation**: Calculate estimated days remaining for each resource based on configurable daily consumption rates.
*   **Persistent State**: Saves and loads resource data to a local JSON file.
*   **Simple CLI**: Easy-to-use command-line interface for quick updates.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is self-contained. Simply navigate to the `utils/rubble-rousers-resource-tracker/src/` directory.

## Usage

Run the `tracker.py` script directly. It will automatically create or load a `tracker_state.json` file in the same directory.

```bash
python src/tracker.py --help
```

### Commands

*   **`init <resource>=<quantity> ...`**: Initialize or overwrite the tracker with new resources. Example: `python src/tracker.py init food=100 water=50 ammo=20`
*   **`add <resource>=<quantity> ...`**: Add quantities to existing or new resources. Example: `python src/tracker.py add food=20 water=10`
*   **`consume <resource>=<quantity> ...`**: Consume quantities from resources. Will warn if not enough. Example: `python src/tracker.py consume food=5 water=3 ammo=1`
*   **`levels`**: Display current levels of all tracked resources. Example: `python src/tracker.py levels`
*   **`estimate <resource>=<daily_consumption> ...`**: Estimate survival days for resources based on daily consumption rates. Example: `python src/tracker.py estimate food=10 water=5 ammo=2`

### Example Workflow

```bash
# Start a new tracker with initial supplies
python src/tracker.py init rations=150 water_purified=75 power_cells=10

# Scavenge some more supplies
python src/tracker.py add rations=50 water_purified=25

# Use up some resources during the day
python src/tracker.py consume rations=10 water_purified=5 power_cells=1

# Check current inventory
python src/tracker.py levels

# Plan for the next few days with estimated daily usage
python src/tracker.py estimate rations=12 water_purified=6 power_cells=1.5
```

## Development

To run tests:

```bash
python -m unittest tests/test_tracker.py
```
