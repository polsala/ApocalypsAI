# Wasteland Wanderer's Wayfinder

Navigate the treacherous post-apocalyptic landscape with ease! The Wasteland Wanderer's Wayfinder is a command-line utility that helps you find the shortest, safest path between two points on a grid, avoiding hazardous zones. Whether you're scavenging for supplies or escaping a horde of irradiated squirrels, this tool will guide your way.

## Features

*   **Grid-based Pathfinding**: Define your wasteland as a grid of specified dimensions.
*   **Hazard Avoidance**: Mark specific coordinates as impassable hazards (e.g., mutant nests, radiation zones, bottomless pits).
*   **Shortest Path Calculation**: Utilizes the A* algorithm to find the most efficient route.
*   **Clear Output**: Visualizes the grid and the calculated path.

## Installation

This utility is self-contained and requires Python 3.8+ (compatible with 3.11). No external dependencies are needed beyond standard Python libraries.

1.  Navigate to the `utils/wasteland-wanderers-wayfinder/` directory.
2.  Ensure you have Python installed.

## Usage

Run the `wayfinder.py` script from the `src/` directory.

```bash
python src/wayfinder.py --grid-width <width> --grid-height <height> \
    --start <x_start>,<y_start> --end <x_end>,<y_end> \
    [--hazard <x1>,<y1> [--hazard <x2>,<y2> ...]]
```

### Arguments:

*   `--grid-width <int>`: The width of the grid (number of columns).
*   `--grid-height <int>`: The height of the grid (number of rows).
*   `--start <x>,<y>`: The starting coordinates (0-indexed).
*   `--end <x>,<y>`: The ending coordinates (0-indexed).
*   `--hazard <x>,<y>`: (Optional, can be repeated) Coordinates of a hazardous zone.

### Example

Find a path on a 10x10 grid from (0,0) to (9,9), avoiding (2,2) and (2,3):

```bash
python src/wayfinder.py --grid-width 10 --grid-height 10 \
    --start 0,0 --end 9,9 \
    --hazard 2,2 --hazard 2,3
```

### Output Example

```
Wasteland Grid (10x10):
S . . . . . . . . .
# . . . . . . . . .
# . X X . . . . . .
# # # # # # # # # .
. . . . . . . . # .
. . . . . . . . # .
. . . . . . . . # .
. . . . . . . . # .
. . . . . . . . # .
. . . . . . . . # E

Path found!
S # . . . . . . . . .
. # . . . . . . . . .
. # X X . . . . . . .
. # # # # # # # # . .
. . . . . . . . # . .
. . . . . . . . # . .
. . . . . . . . # . .
. . . . . . . . # . .
. . . . . . . . # . .
. . . . . . . . # E

Path length: 18 steps
```

Where:
*   `S`: Start
*   `E`: End
*   `X`: Hazard
*   `#`: Path
*   `.`: Empty space
