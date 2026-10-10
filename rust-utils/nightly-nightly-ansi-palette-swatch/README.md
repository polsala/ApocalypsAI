# nightly-ansi-palette-swatch

Utility that prints a range of 256‑color ANSI palette blocks with their color codes, useful for terminal theming and whimsical color exploration.

## Usage

```sh
nightly-ansi-palette-swatch          # prints all 0‑255 colors
nightly-ansi-palette-swatch 16 31    # prints colors 16‑31
```

The tool outputs each color as a colored block followed by its code.

## Build & Run

```sh
cargo build --release
./target/release/nightly-ansi-palette-swatch [START] [END]
```

## License

MIT
