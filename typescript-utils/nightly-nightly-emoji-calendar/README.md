# nightly-emoji-calendar

A tiny, whimsical TypeScript CLI that prints a month calendar with each weekday replaced by a cute emoji.

## Features

- Generates a calendar for any month/year (defaults to current month).
- Weekdays are shown as emojis: 
  - Sunday: âï¸
  - Monday: ð
  - Tuesday: ð
  - Wednesday: ð
  - Thursday: ð
  - Friday: ð
  - Saturday: ð¸
- Zeroâdependency, runs with `ts-node` (or after compilation).

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-calendar

# Install dev dependencies (jest for tests, ts-node for execution)
npm install
```

## Usage

```bash
# Run directly with ts-node
npx ts-node src/index.ts            # current month
npx ts-node src/index.ts 9 2025   # September 2025

# After compilation
npm run build
node dist/index.js 12 2023
```

## Example Output

```text
      September 2025
âï¸ ð ð ð ð ð ð¸
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30
```

## Testing

```bash
npm test
```

The test suite checks that the generated calendar string contains the correct emojis and day counts for known months.

## License

MIT Â© ApocalypsAI
