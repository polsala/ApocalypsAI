# nightly-ansi-palette-picker

A whimsical yet handy CLI that converts common color names into their nearest ANSI 256-color code and prints a colorful sample block in the terminal.

## Installation

```sh
npm install -g .
```

(Assumes you are in the utility directory.)

## Usage

```sh
node src/index.js <color-name>
```

Example:

```sh
$ node src/index.js teal
Color: teal → ANSI 256 code: 6
Sample: █
```

The utility also exports a `getAnsiCode(colorName)` function for programmatic use.

## Supported colors

- black, maroon, green, olive, navy, purple, teal, silver, grey, red, lime, yellow, blue, fuchsia, aqua, white
- orange, pink, brown, gold, cyan, magenta

## Testing

```sh
npm test
```

Runs the Node test suite which validates the color‑to‑code mapping.
