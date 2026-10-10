# nightly-ansi-palette-swatch

A tiny Rust CLI that prints a swatch of ANSI 256‑color codes to your terminal. Useful for picking colors for scripts, themes, or just for fun.

## Usage

```sh
# Print all 256 colors
nightly-ansi-palette-swatch

# Print a subset, e.g., colors 16‑31
nightly-ansi-palette-swatch --range 16-31
```

## Options

- `--range START-END` – inclusive range of color codes (0‑255). Defaults to `0-255`.

## Build & Run

```sh
cargo build --release
./target/release/nightly-ansi-palette-swatch [--range START-END]
```
