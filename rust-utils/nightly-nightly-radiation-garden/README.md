# nightly‑radiation‑garden

**A whimsical Rust CLI for post‑apocalyptic gardeners**

When the world has gone a little radioactive, you still want fresh veggies. This tool takes a location name and a radiation level (`low`, `medium`, or `high`) and prints a short list of plants that are likely to survive.

## Installation

```bash
# Ensure you have Rust installed (https://rustup.rs)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-radiation-garden
cargo build --release
```

The binary will be at `target/release/nightly-radiation-garden`.

## Usage

```bash
./target/release/nightly-radiation-garden "Wasteland Outpost" high
```

Output example:

```
Location: Wasteland Outpost
Radiation level: high
Recommended plants:
 - Radish (tolerates high radiation)
 - Sunflower (absorbs contaminants)
 - Kale (hardy leafy green)
```

## How it works

The program contains a tiny hard‑coded lookup table mapping radiation levels to a few hardy plants. It is deliberately simple – the goal is to be a fun, self‑contained example of a Rust CLI utility.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.
