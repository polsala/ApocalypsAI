# Wasteland Scavenger Planner

A crucial utility for any survivor navigating the treacherous post-apocalyptic landscape! The Wasteland Scavenger Planner helps you plot the safest and most efficient routes to valuable resources, all while steering clear of irradiated zones, mutant nests, and other unspeakable horrors.

## Features

*   **Grid-based Pathfinding**: Navigate simple text-based maps.
*   **Hazard Avoidance**: Automatically avoids 'X' marked danger zones.
*   **Resource Prioritization**: Finds paths to 'R' (resources) or 'E' (exit/safe zone).
*   **Clear Path Visualization**: See your optimal route marked on the map.

## How to Use

1.  **Define Your Map**: Create a text file or a Python list of strings representing your wasteland.
    *   `S`: Your starting position.
    *   `E`: Your designated exit or safe zone.
    *   `R`: A valuable resource you need to scavenge.
    *   `X`: An impassable hazard (e.g., radiation, mutant lair).
    *   `.`: A clear, traversable path.
    *   Any other character will be treated as an impassable obstacle.

2.  **Run the Planner**:
    ```bash
    python src/planner.py
    ```
    The script will prompt you to input your map, or you can modify `src/planner.py` to load a predefined map.

### Example Map Input:

```
S.R
.X.
E..
```

### Example Output:

```
Map:
S.R
.X.
E..

--- Planning Results ---
Path found! Length: 1 steps.
Path visualization:
S>R
.X.
E..
```

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required.
