# nightly-ansi-palette-swatch

A whimsical yet handy CLI utility that prints the full 256‑color ANSI palette as colored blocks in your terminal.

## Why?

When working with terminal applications, picking the right ANSI color can be a guessing game. This tool gives you a quick visual reference, perfect for theming scripts, logs, or just adding a splash of post‑apocalyptic flair.

## Installation

```sh
npm install -g ts-node typescript
git clone <repo> && cd nightly-ansi-palette-swatch
npm install
```

Or run directly without installing:

```sh
npx ts-node src/index.ts
```

## Usage

```sh
$ npx ts-node src/index.ts
```

The output is a 16×16 grid where each cell shows its color code padded to three digits.

## License

MIT
