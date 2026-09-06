# Nightly Scavenger Swarm Coordinator

## Summary
`nightly-scavenger-swarm-coord` is a whimsical-yet-useful Go utility that simulates dispatching a swarm of 'scavenger bots' to concurrently search various 'zones' for a specified 'resource'. It leverages Go's goroutines and channels to perform these simulated searches in parallel, reporting on the success or failure of each bot.

This tool is great for demonstrating basic Go concurrency patterns (goroutines, wait groups, channels) in a fun, post-apocalyptic context.

## How it Works
1.  **Target & Zones**: You provide a target resource (e.g., "water filter", "scrap metal") and a list of zones to search.
2.  **Scavenger Bots (Goroutines)**: For each zone, a separate goroutine is launched, acting as an independent scavenger bot.
3.  **Simulated Search**: Each bot 'searches' its assigned zone. The search is simulated against a predefined, internal `ZoneContents` map. It also includes a simulated, variable delay to mimic real-world search times or network latency.
4.  **Results (Channels)**: Results from each scavenger bot (whether the resource was found, and a message) are sent back through a Go channel.
5.  **Summary**: Once all bots have reported back, the utility prints a summary of findings, indicating which zones yielded the resource and which did not.

## Installation & Usage

### Prerequisites
-   Go (version 1.16 or higher)

### Build
To build the executable, navigate to the utility's directory and run:

```bash
go build -o nightly-scavenger-swarm-coord src/main.go
```

### Run
Execute the compiled binary with your desired target resource and a list of zones:

```bash
./nightly-scavenger-swarm-coord "water filter" "Abandoned Mall" "Overgrown Park" "Old Factory"
```

**Example Output:**
```
Dispatching scavenger swarm to find 'water filter' across 3 zones...
[FAILURE] 'water filter' not found in Old Factory.
[SUCCESS] Found 'water filter' in Abandoned Mall!
[FAILURE] 'water filter' not found in Overgrown Park.

--- Scavenge Summary ---
Successfully located 'water filter' in 1 out of 3 zones.
```

**Available Simulated Zones & Resources (case-insensitive search):**
-   **Old Factory**: `scrap metal`, `wires`, `rusty tools`
-   **Abandoned Mall**: `canned food`, `water filter`, `first aid kit`, `clothing`
-   **Overgrown Park**: `herbs`, `wild berries`, `fresh water source`
-   **Collapsed Bridge**: `rope`, `climbing gear`
-   **Silent Library**: `books`, `maps`, `old records`

## Testing
To run the automated tests, navigate to the utility's directory and run:

```bash
go test ./...
```

All tests are deterministic and offline, using a mock `ZoneContents` map to simulate resource availability without external dependencies.
