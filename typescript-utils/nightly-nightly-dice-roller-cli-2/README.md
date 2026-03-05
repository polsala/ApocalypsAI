# nightly-dice-roller-cli

Roll dice using RPG notation (e.g., `2d6+1`) and display each die as ASCII art.

## Installation

```sh
npm install -g .
# or run directly with ts-node
npx ts-node src/main.ts 2d6+1
```

## Usage

```sh
npx ts-node src/main.ts 3d8-2
```

The tool parses the notation, rolls the dice, prints each die face in ASCII, and shows the total including any modifier.

## Example

```
$ npx ts-node src/main.ts 2d6+3
+-------+   +-------+
| *   * |   | *   * |
|   *   | + |   *   |
| *   * |   | *   * |
+-------+   +-------+
Rolls: [4,5] Modifier: +3 Total: 12
```

## License

MIT
