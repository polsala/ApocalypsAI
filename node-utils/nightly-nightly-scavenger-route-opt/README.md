# Nightly Scavenger Route Optimizer

A whimsical-yet-useful CLI tool designed to help survivors optimize their scavenging routes in the wasteland. Given a starting point and a list of known resource locations, it calculates an efficient path using a nearest-neighbor heuristic.

## Features

*   **Route Optimization**: Calculates a sequential route to visit all specified resource locations.
*   **Distance Calculation**: Uses Euclidean distance to determine the shortest path between points.
*   **CLI Interface**: Easy to use from the command line.

## Installation

1.  Navigate to the `node-utils/nightly-scavenger-route-opt` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line, providing your starting X and Y coordinates, and the path to a JSON file containing resource locations.

```bash
node src/index.js <startX> <startY> <resourceFilePath>
```

**Arguments:**

*   `<startX>`: Your current X coordinate (e.g., `10`).
*   `<startY>`: Your current Y coordinate (e.g., `20`).
*   `<resourceFilePath>`: The path to a JSON file listing resource locations.

### Resource File Format

The resource file should be a JSON array of objects, where each object represents a location with a `name`, `x` coordinate, and `y` coordinate.

**`resources.json` example:**

```json
[
  {
    "name": "Abandoned Bunker",
    "x": 1,
    "y": 1
  },
  {
    "name": "Water Source",
    "x": 10,
    "y": 0
  },
  {
    "name": "Food Cache",
    "x": 0,
    "y": 5
  },
  {
    "name": "Old Pharmacy",
    "x": 7,
    "y": 8
  }
]
```

### Example Run

```bash
node src/index.js 0 0 ./resources.json
```

**Expected Output:**

```
--- Optimized Scavenging Route ---
1. Start (0, 0)
2. Abandoned Bunker (1, 1)
3. Food Cache (0, 5)
4. Old Pharmacy (7, 8)
5. Water Source (10, 0)
Total estimated travel distance: 20.37 units
```

## Development

### Running Tests

To run the automated tests, use:

```bash
npm test
```
