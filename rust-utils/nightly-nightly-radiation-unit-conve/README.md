# Radiation Unit Converter

`radiation-unit-converter` is a tiny, zero‑dependency (aside from `clap`) Rust CLI that converts radiation measurements between the most common units:

- Sievert (Sv)
- Millisievert (mSv)
- Microsievert (µSv)
- Rem
- Rad

## Installation

```bash
# Install via Cargo (requires Rust toolchain)
cargo install radiation-unit-converter --git https://github.com/polsala/ApocalypsAI.git --locked
```

> **Note**: The utility lives under the `rust-utils/nightly-radiation-unit-converter` directory in the repository. The above command clones the repo and builds the binary.

## Usage

```bash
# Convert 1 Sv to mSv
radiation-unit-converter 1 Sv mSv
# → 1000.000000 mSv

# Convert 5 rem to rad (they are equivalent)
radiation-unit-converter 5 rem rad
# → 5.000000 rad
```

The tool prints the converted value with six decimal places followed by the target unit.

## How it works

The program parses three positional arguments:
1. The numeric value (`f64`).
2. The source unit (case‑insensitive, accepts `Sv`, `mSv`, `µSv`, `rem`, `rad`).
3. The destination unit.

Internally it normalises the input to Sieverts and then converts to the requested unit.

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.
