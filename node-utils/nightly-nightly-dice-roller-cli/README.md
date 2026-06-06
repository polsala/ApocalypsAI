# nightly-dice-roller-cli

Roll dice using standard RPG notation (e.g., `2d6+3`) from the command line.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js 2d6+3
```

If no argument is provided, defaults to `1d6`.

## How it works

- Parses `<count>d<sides>` optionally followed by `+<modifier>` or `-<modifier>`.
- Uses cryptographically secure random numbers.

## License

MIT
