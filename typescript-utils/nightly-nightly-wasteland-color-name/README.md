# Nightly Wasteland Color Namer

A whimsical TypeScript CLI that turns a hex color code into an apocalypse‑themed name, e.g. `#ff4500` → `Scorching Ember`. Useful for designers who want a gritty label for their palette.

## Installation

```sh
npm install -g ts-node typescript
```

## Usage

```sh
npx ts-node src/index.ts <hex-color>
```

Example:

```sh
$ npx ts-node src/index.ts #ff0000
Scorching Ember
```

## How it works

The tool analyses the RGB components and picks an adjective based on the brightest channel and a noun based on the dominant channel.

## License

MIT
