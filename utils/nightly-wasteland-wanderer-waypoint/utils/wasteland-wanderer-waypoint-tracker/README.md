# Wasteland Wanderer's Waypoint Tracker

## Description

In a world reshaped by chaos, reliable navigation and resource tracking are paramount. The `Wasteland Wanderer's Waypoint Tracker` is a lightweight, command-line utility designed to help you keep tabs on crucial locations, safe havens, and points of interest. Whether you're marking a cache of canned goods, a fresh water source, or the lair of a particularly grumpy mutant, this tracker ensures your vital waypoints are always at your fingertips.

It stores waypoints with a name, latitude, longitude, and optional notes in a simple, local JSON file.

## Usage

### Prerequisites

*   Python 3.8+

### Installation

No installation needed! Just place the `src/tracker.py` file in your desired location and make it executable, or run it directly with `python`.

### Commands

The `tracker.py` script supports the following commands:

*   **`python src/tracker.py add <name> <latitude> <longitude> [notes...]`**
    *   Adds a new waypoint.
    *   `<name>`: A unique identifier for the waypoint (e.g., "Old_Gas_Station").
    *   `<latitude>`: The latitude coordinate (e.g., "34.0522").
    *   `<longitude>`: The longitude coordinate (e.g., "-118.2437").
    *   `[notes...]`: Optional descriptive notes (can be multiple words, will be joined).

    *Example:*
    ```bash
    python src/tracker.py add "Safe_House_Alpha" "34.0522" "-118.2437" "Abandoned library, good for shelter, watch out for feral cats."
    ```

*   **`python src/tracker.py list`**
    *   Lists all stored waypoints with their names, coordinates, and a snippet of notes.

    *Example:*
    ```bash
    python src/tracker.py list
    ```

*   **`python src/tracker.py get <name>`**
    *   Retrieves and displays the full details for a specific waypoint.
    *   `<name>`: The name of the waypoint to retrieve.

    *Example:*
    ```bash
    python src/tracker.py get "Safe_House_Alpha"
    ```

*   **`python src/tracker.py delete <name>`**
    *   Removes a waypoint from your tracker.
    *   `<name>`: The name of the waypoint to delete.

    *Example:*
    ```bash
    python src/tracker.py delete "Old_Gas_Station"
    ```

## Data Storage

Waypoints are stored in a JSON file named `waypoints.json` in the same directory as `tracker.py`. This file is automatically created if it doesn't exist.
