# Nightly ANSI Palette Swatch

A whimsical CLI utility that prints the full 256‑color ANSI palette in your terminal, each color labeled with its code. Great for picking terminal colors in the post‑apocalyptic wasteland.

## Installation

```sh
npm install -g nightly-ansi-palette-swatch
```

## Usage

```sh
npx nightly-ansi-palette-swatch
```

or, if installed globally:

```sh
ansi-palette-swatch
```

The tool prints a grid of colors; each cell shows the color code in its own color.

## How it works

The utility generates ANSI escape sequences for the 256‑color mode and formats them into a 16‑column grid.

## License

MIT
