# Wasteland Wanderer's Waypoint Mapper

Navigate the desolate future with confidence! The `nightly-wasteland-waypoint-mapper` is a simple command-line utility designed to help you track and manage crucial locations across the ravaged landscape. Whether it's a hidden cache of supplies, a rumored safe zone, or a known mutant nest, keep your waypoints organized and accessible.

## Features

*   **Add Waypoints**: Record new locations with a name, coordinates, and a description.
*   **List Waypoints**: View all your saved waypoints.
*   **Find Waypoint**: Quickly retrieve details for a specific location by name.
*   **Delete Waypoint**: Remove outdated or no-longer-relevant waypoints.
*   **Persistent Storage**: All waypoints are saved to a local JSON file, so your intel survives reboots (and minor skirmishes).

## Installation

This utility is self-contained and written in Python 3.11. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-wasteland-waypoint-mapper/` directory.
2.  You can run the script directly:
    ```bash
    python src/mapper.py --help
    ```

## Usage

The `mapper.py` script uses subcommands for different operations. By default, it uses `waypoints.json` in the current directory for storage, but you can specify a different file using `--data-file`.

```bash
python src/mapper.py [command] [options]
```

### Commands:

#### `add <name> <coords> <description>`
Adds a new waypoint.

*   `<name>`: A unique name for the waypoint (e.g., "Old Gas Station").
*   `<coords>`: Coordinates (e.g., "N34.05,W118.25", "-34.05,118.25").
*   `<description>`: A brief description of the location.

**Example:**
```bash
python src/mapper.py add "Vault 77" "N38.90,W77.03" "Rumored pre-war vault, possibly intact. High radiation." --data-file my_wasteland_map.json
```

#### `list`
Lists all saved waypoints.

**Example:**
```bash
python src/mapper.py list --data-file my_wasteland_map.json
```

#### `find <name>`
Finds and displays details for a specific waypoint.

*   `<name>`: The name of the waypoint to find.

**Example:**
```bash
python src/mapper.py find "Vault 77" --data-file my_wasteland_map.json
```

#### `delete <name>`
Deletes a waypoint by name.

*   `<name>`: The name of the waypoint to delete.

**Example:**
```bash
python src/mapper.py delete "Old Gas Station" --data-file my_wasteland_map.json
```

## Development

To run tests, navigate to the `utils/nightly-wasteland-waypoint-mapper/` directory and execute:

```bash
python -m unittest tests/test_mapper.py
```
