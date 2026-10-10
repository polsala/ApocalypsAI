# Nightly Scavenger Map

**Utility:** `nightly-scavenger-map`

Generate a whimsical, random ASCII map that can be used for post‑apocalypse scavenging games, tabletop sessions, or just for fun.

## Features
- Adjustable width and height.
- Optional `--seed` flag for deterministic maps (great for testing or sharing the same map).
- Simple symbols:
  - `.` – empty ground
  - `W` – water source
  - `F` – food cache
  - `M` – medical supplies
  - `T` – tools / equipment

## Installation
```sh
# Clone the repository (or copy the generated folder) and build with Cargo
cargo build --release
```

## Usage
```sh
# Basic usage – random map each run
cargo run --release -- <width> <height>

# Example: 20 columns by 10 rows
cargo run --release -- 20 10

# Reproducible map with a seed
cargo run --release -- 20 10 --seed 12345
```

## Testing
```sh
cargo test
```

The test suite checks that the map dimensions are correct and that only the allowed symbols appear.

## License
MIT – see the LICENSE file in the repository.
