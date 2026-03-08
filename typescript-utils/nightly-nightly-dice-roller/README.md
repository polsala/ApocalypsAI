# nightly-dice-roller

Roll dice using RPG notation (e.g., `2d6+3`) and see each die rendered as a Unicode face.

## Installation

```sh
npm install -g nightly-dice-roller
```

## Usage

```sh
npx nightly-dice-roller 3d8+2
```

Typical output:

```
🎲 3d8+2 → [⚂ ⚅ ⚁] + 2 = 13
```

## Notation

- `NdM` rolls **N** dice each with **M** sides.
- An optional `+K` or `-K` modifier adds/subtracts a constant.
- If **N** is omitted it defaults to `1` (e.g., `d20`).

## Development

Run the test suite:

```sh
npm test
```

The project is a single‑file TypeScript CLI with no external dependencies.
