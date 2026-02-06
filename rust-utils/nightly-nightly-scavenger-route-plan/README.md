# nightly-scavenger-route-planner

A tiny Rust CLI that takes a comma‑separated list of location names and prints a scavenger route.

## Features

- Accepts a list of locations via a command‑line argument.
- By default, returns the locations in reverse order (deterministic, easy to test).
- With the `--shuffle` flag, the order is randomized using the `rand` crate.
- Outputs one location per line, ready to be copied into a map or game session.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone <repo-url>
cd nightly-scavenger-route-planner
cargo build --release
```

The binary will be at `target/release/scavenger-route-planner`.

## Usage

```bash
# Deterministic reverse route
./scavenger-route-planner "Base,Warehouse,Outpost,Radio Tower"

# Randomized route
./scavenger-route-planner --shuffle "Base,Warehouse,Outpost,Radio Tower"
```

## Example Output

```
Radio Tower
Outpost
Warehouse
Base
```

## Testing

```bash
cargo test
```

The test suite checks the deterministic behavior.
