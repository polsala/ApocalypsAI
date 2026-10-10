# nightly-dice-roller-cli

A whimsical command‑line utility written in TypeScript that parses classic dice notation (e.g., `2d6+3`) and prints the roll result. Useful for tabletop gamers, developers testing random logic, or anyone who likes a quick dice roll from the terminal.

## Installation

```sh
npm install -g nightly-dice-roller-cli
```

## Usage

```sh
npx nightly-dice-roller-cli 3d8+2
```

Outputs something like:

```
Rolling 3d8+2 => [5, 7, 2] + 2 = 16
```

## Development

Run the tests:

```sh
npm test
```
