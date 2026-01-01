# Nightly Scavenger Map

**Utility:** `nightly-scavenger-map`

## Overview

A tiny Rust CLI that creates a random ASCII‑art map populated with scavenging resources (food, water, medicine, etc.). Perfect for tabletop RPGs, improv storytelling, or just a fun way to visualise a post‑apocalyptic landscape.

## Features

- Configurable width and height.
- Choose which resource symbols to sprinkle on the map.
- Optional deterministic seed for reproducible maps (great for testing or sharing).
- Zero‑runtime dependencies beyond the standard library and the lightweight `rand` crate.

## Installation

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-scavenger-map

# Build the binary
cargo build --release
```

The compiled binary will be located at `target/release/nightly-scavenger-map`.

## Usage

```bash
nightly-scavenger-map [options]
```

### Options

- `-w <width>`   : Map width (default: `10`).
- `-h <height>`  : Map height (default: `5`).
- `-r <list>`    : Comma‑separated list of single‑character resource symbols (default: `F,W,M` for Food, Water, Medicine).
- `-s <seed>`    : Optional numeric seed for deterministic output.
- `-h` or `--help`: Show help.

### Example

```bash
nightly-scavenger-map -w 12 -h 6 -r F,W,M -s 42
```

Possible output:

```
...........F
..W..........
.............
....M........
.............
.............
```

Each run with the same seed will produce the identical map.

## Testing

Run the test suite with:

```bash
cargo test
```

The integration test checks that a known seed yields a predictable map layout.

---

*Enjoy your wanderings through the wasteland!*
