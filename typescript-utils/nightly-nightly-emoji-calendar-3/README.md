# nightly-emoji-calendar

**Emoji Calendar Generator**

A tiny commandâline utility that prints a month calendar with each day decorated by an emoji representing its weekday.

## Emojis used
| Weekday | Emoji |
|---------|-------|
| Sunday    | âï¸ |
| Monday    | ð |
| Tuesday   | ð |
| Wednesday | ð |
| Thursday  | ð |
| Friday    | ð |
| Saturday  | ð |

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-calendar
# Install dependencies (none required beyond Node.js)
# Ensure you have Node.js >= 14 installed
```

## Usage

```bash
# Run for the current month
node src/emoji-calendar.js

# Specify month and year (month is 1â12)
node src/emoji-calendar.js 5 2024
```

The program prints a header like `Emoji Calendar for 5/2024` followed by a grid where each cell looks like `ð15` (emoji + twoâdigit day). Empty cells are three spaces.

## API

The core function can be imported in other TypeScript/JavaScript projects:

```ts
import { generateCalendar } from './emoji-calendar';
const lines = generateCalendar(12, 2025);
console.log(lines.join('
'));
```

## Testing

Run the bundled test with Node:

```bash
node tests/test_emoji-calendar.js
```

The test checks that Januaryâ¯2023 (where the 1st is a Sunday) starts with the expected `âï¸01` token.

## License

MIT Â© ApocalypsAI
