# nightly-ansi-color-palette

A tiny Rust CLI that prints the full 256âcolor ANSI palette.

## Features

- **Pretty mode** (default): prints a grid of colored blocks with their numeric codes.
- **JSON mode**: `--json` outputs a JSON array of objects `{ "code": <u8>, "sample": "[38;5;<code>mâ[0m" }`.

## Installation

```bash
# Clone the utility
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-ansi-color-palette

# Build with Cargo
cargo build --release

# The binary will be at target/release/ansi-color-palette
```

## Usage

```bash
# Pretty grid (default)
./ansi-color-palette

# JSON output
./ansi-color-palette --json
```

## Example output (pretty mode)

````
0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
... (continues up to 255)
````

## Testing

```bash
cargo test
```

## License

MIT
