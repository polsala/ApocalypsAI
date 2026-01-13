# Nightly Cryptic Hash Visualizer

## Overview

`nightly-cryptic-hash-visualizer` is a tiny TypeScript CLI that takes any input string, computes its SHAâ256 hash, and renders a playful visual fingerprint using block characters (â, â, â, â).  Itâs handy when you want a quick, humanâreadable âartisticâ representation of a hash without leaving the terminal.

## Installation

```bash
# Clone the utility (or copy the folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-cryptic-hash-visualizer

# Install dependencies
npm install

# (Optional) Install globally for easy access
npm link
```

## Usage

```bash
# Run via npx (no global install needed)
npx nightly-cryptic-hash-visualizer "your secret phrase"

# If installed globally
nightly-cryptic-hash-visualizer "your secret phrase"
```

The command prints four rows of block characters, each row 16 characters wide, representing the hash.

## Example

```bash
$ nightly-cryptic-hash-visualizer "hello world"
ââââââââââââââââ
ââââââââââââââââ
ââââââââââââââââ
ââââââââââââââââ
```

## How It Works

1. The input string is hashed with SHAâ256 using Node's builtâin `crypto` module.
2. Each hexadecimal digit (0âf) is mapped to a block character: 
   - `0â3` â `â` (light)
   - `4â7` â `â` (mediumâlight)
   - `8âb` â `â` (mediumâdark)
   - `câf` â `â` (dark)
3. The 64âcharacter hex digest becomes 64 block characters, formatted into four rows of 16.

## Testing

```bash
npm test
```

The test suite verifies that a known input produces the expected visual output.

## License

MIT â see the LICENSE file in the repository root.
