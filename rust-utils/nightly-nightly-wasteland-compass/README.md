# nightly‑wasteland‑compass

**nightly‑wasteland‑compass** is a tiny Rust CLI tool that takes your current compass bearing (in degrees) and applies a random “radiation drift” to simulate the chaotic navigation of a wasteland wanderer.

## Features

- Accepts an optional current bearing (default 0°).
- Accepts an optional maximum drift range (default 30°).
- Uses a deterministic pseudo‑random generator so tests are reproducible.
- Outputs the new bearing in the range 0‑359°.

## Installation

```bash
# From the repository root
cd rust-utils/nightly-wasteland-compass
cargo build --release
# The binary will be at target/release/nightly-wasteland-compass
```

## Usage

```bash
# Basic usage – defaults to 0° bearing and 30° max drift
./nightly-wasteland-compass

# Specify a current bearing
./nightly-wasteland-compass --bearing 90

# Specify a max drift (e.g., up to 45°)
./nightly-wasteland-compass --bearing 180 --max-drift 45
```

The program prints something like:

```
Current bearing: 180°
Drift applied: -12°
New bearing: 168°
```

## Testing

```bash
cargo test
```

The tests use a fixed seed to guarantee deterministic output.

## License

MIT © ApocalypsAI community
