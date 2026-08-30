# Nightly Cosmic Commute Planner

Navigate the vast, unpredictable cosmos with confidence! The `nightly-cosmic-commute-plan` is a whimsical CLI utility designed to help you plan your interstellar journeys, simulating various cosmic phenomena that might affect your travel time. Whether you're dodging asteroid fields or harnessing gravity assists, this tool will chart your course.

## Features

-   **Celestial Waypoint Network:** A predefined network of cosmic locations and routes.
-   **Anomaly Simulation:** Randomly applies "cosmic events" like solar flares (delays) or gravity assists (speed boosts) to routes.
-   **Optimal Pathfinding:** Uses a modified Dijkstra's algorithm to find the quickest path, considering potential anomalies.
-   **Interactive CLI:** Easily specify your starting point and destination.

## Installation

1.  Ensure you have Node.js installed (v14 or higher).
2.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-cosmic-commute-plan
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Make the script executable (optional, for direct execution):
    ```bash
    chmod +x src/index.js
    ```

## Usage

Run the utility from its directory:

```bash
node src/index.js <start_waypoint> <end_waypoint> [--seed <number>]
```

**Arguments:**

-   `<start_waypoint>`: The name of your starting celestial waypoint (e.g., "Earth_Orbital_Hub").
-   `<end_waypoint>`: The name of your destination celestial waypoint (e.g., "Mars_Outpost").
-   `--seed <number>`: (Optional) A numeric seed for the random anomaly generator, ensuring reproducible results.

**Example:**

```bash
node src/index.js Earth_Orbital_Hub Jupiter_Mining_Colony
```

```bash
node src/index.js Alpha_Centauri_Gateway Andromeda_Nexus --seed 123
```

### Available Waypoints

-   `Earth_Orbital_Hub`
-   `Lunar_Refueling_Station`
-   `Mars_Outpost`
-   `Jupiter_Mining_Colony`
-   `Saturn_Ring_Resort`
-   `Alpha_Centauri_Gateway`
-   `Orion_Nebula_Observatory`
-   `Andromeda_Nexus`

## How it Works

The utility defines a graph where waypoints are nodes and routes are edges with base travel times. When planning a commute, it simulates cosmic anomalies for each route. These anomalies can either increase (e.g., "Solar Flare Delay") or decrease (e.g., "Gravity Assist Boost") the travel time. A Dijkstra-like algorithm then finds the path with the minimum *simulated* total travel time.

## Development

To run tests:

```bash
npm test
```
