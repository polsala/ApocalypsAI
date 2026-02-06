# nightly-roman-numeral-converter

A tiny TypeScript utility that converts integers to Roman numerals and vice‑versa.

## Features

- `intToRoman(num: number): string` – Convert an integer (1‑3999) to its Roman numeral representation.
- `romanToInt(str: string): number` – Parse a Roman numeral (case‑insensitive) back to an integer.
- Command‑line interface `roman` for quick conversions.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install dependencies
npm install
```

> **Note**: The utility has no external runtime dependencies; the `npm install` step only creates a `node_modules` folder for development tools (e.g., `ts-node` if you wish to run the TypeScript source directly).

## Build

Compile the TypeScript sources to JavaScript:

```bash
npx tsc
```

This will generate `src/roman.js` and `src/cli.js`.

## Usage

```bash
# After building, run the CLI
node src/cli.js 1994        # => MCMXCIV
node src/cli.js MCMXCIV    # => 1994
```

You can also use the library programmatically:

```ts
import { intToRoman, romanToInt } from './src/roman';

console.log(intToRoman(58)); // LVIII
console.log(romanToInt('LVIII')); // 58
```

## Testing

Run the bundled tests with Node:

```bash
node tests/roman.test.js
```

All tests should pass and output `All tests passed`.

## License

MIT © ApocalypsAI
