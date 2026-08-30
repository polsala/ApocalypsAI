# Scavenger Route Planner

A whimsical CLI tool that takes a list of locations and generates a random scavenger route with distances between each stop. Perfect for post‑apocalypse adventures or fun road‑trip planning.

## Installation

```sh
cargo build --release
```

## Usage

```sh
./target/release/scavenger-route-planner "Abandoned Mall,Radio Tower,Underground Bunker,Old Library"
```

The program will output a shuffled route with random distances (1‑10 km) between consecutive locations.

## Testing

```sh
cargo test
```
