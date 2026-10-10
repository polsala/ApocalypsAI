# Nightly Scavenger Drone Coordinator

## Overview

The `nightly-scavenger-drone-coord` is a whimsical-yet-useful utility designed to simulate and coordinate resource collection from various "wasteland zones" using autonomous "scavenger drones." It demonstrates concurrent task execution and result aggregation using Go's goroutines and channels.

In a post-apocalyptic world, efficient resource gathering is paramount. This tool helps you manage a fleet of simulated drones, dispatching them to different areas and collecting their findings in a structured report. While the scavenging itself is simulated, the underlying concurrency model is robust and applicable to real-world distributed task management.

## Features

*   **Concurrent Dispatch**: Drones are dispatched to zones concurrently, maximizing efficiency.
*   **Result Aggregation**: Collects findings from all drones into a single, comprehensive report.
*   **Error Handling**: Reports zones where drones encountered issues (simulated temporal anomalies).
*   **Configurable Zones**: Easily specify which zones your drones should explore.

## Usage

### Prerequisites

*   Go (version 1.16 or higher)

### Build

Navigate to the utility's directory and build the executable:

```bash
go build -o scavenger-coord src/main.go
```

### Run

Execute the compiled program, providing a comma-separated list of zones to scavenge:

```bash
./scavenger-coord --zones "Old City Ruins,Toxic Mire,Forgotten Bunker,Whispering Canyons"
```

**Example Output:**

```
Dispatching scavenger drones to 4 zones...

--- Scavenging Report ---
Zone: Old City Ruins | Found: Scrap Metal
Zone: Toxic Mire | Found: Mutated Flora
Zone: Forgotten Bunker | Found: Ancient Tech Part
Zone: Whispering Canyons | Found: Purified Water
-------------------------
```

If a drone encounters a simulated error:

```
Dispatching scavenger drones to 2 zones...

--- Scavenging Report ---
Zone: ZoneA | Found: Pre-War Ration
Zone: ZoneB | Status: FAILED | Error: drone encountered a temporal anomaly in ZoneB
-------------------------
```

## Development

### Code Structure

*   `src/main.go`: Contains the main application logic, including the `ScavengeCoordinator` and the `simulatedScavenge` function.
*   `tests/main_test.go`: Unit tests for the `ScavengeCoordinator`.

### Testing

To run the tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```

The tests use mock functions for the `scavengeAction` to ensure determinism and speed, isolating the coordinator's logic from the simulated random delays and failures of the actual `simulatedScavenge` function.
