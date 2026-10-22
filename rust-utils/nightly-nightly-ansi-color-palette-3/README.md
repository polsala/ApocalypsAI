# nightly-ansi-color-palette

Utility that prints the full 256‑color ANSI palette as colored blocks with their numeric codes. Handy for terminal theming, debugging, or just a splash of color.

## Usage

```sh
cargo run --quiet
```

or after building:

```sh
./target/release/nightly-ansi-color-palette
```

The program outputs rows of 16 colors each, showing the background color and the code.

## Implementation

Implemented in Rust, no external binaries required. Uses standard ANSI escape codes.

## Tests

Run `cargo test` to verify that the generated palette string contains expected codes.
