# nightly-ansi-palette-swatch

Displays the 256‑color ANSI palette in your terminal.

## Usage

```sh
node src/main.js          # prints palette with color blocks
node src/main.js --format=hex   # prints hex codes alongside each swatch
node src/main.js --format=rgb   # prints RGB values alongside each swatch
```

## How it works

The script iterates over color indices 0‑255 and prints a colored block using the ANSI escape sequence `\x1b[38;5;<n>m█\x1b[0m`. When `--format` is supplied, it also prints the corresponding color value (hex or rgb) derived from the xterm 256‑color chart.

## Testing

Run the test suite with:

```sh
node tests/test_main.js
```

The tests verify that the utility produces the expected ANSI sequences for a few sample colors and that the `--format` flag works correctly.
