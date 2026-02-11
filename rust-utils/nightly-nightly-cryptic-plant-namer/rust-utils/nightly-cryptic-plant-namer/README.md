# nightly‑cryptic‑plant‑namer

A tiny Rust CLI that generates whimsical, Latin‑style plant names.  Perfect for writers, game‑masters, or anyone who needs a mysterious flora name on the fly.

## Features

- Randomly combines a botanical adjective with a Latin root.
- Optional `--describe` flag adds a short, fanciful description.
- Zero‑runtime dependencies beyond the standard library and `rand` (used at compile time).

## Installation

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/your‑org/ApocalypsAI.git
cd rust-utils/nightly-cryptic-plant-namer

# Build the binary
cargo build --release
```

The compiled binary will be located at `target/release/cryptic-plant-namer`.

## Usage

```bash
# Generate a plant name
./target/release/cryptic-plant-namer

# Generate a plant name with a description
./target/release/cryptic-plant-namer --describe
```

Example output:

```
Aurea luminosa
A radiant plant that glows faintly at dusk, its leaves shimmering like sunrise.
```

## Testing

```bash
cargo test
```

All tests are deterministic and run offline.
