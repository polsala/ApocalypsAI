# nightly-emoji-timezone-clock

A tiny TypeScript utility that prints the current hour for a specified IANA timezone and adds a fun emoji that reflects the time of day.

## Features
- Accepts any valid IANA timezone (e.g., `America/New_York`, `Asia/Tokyo`).
- Uses the built‑in `Intl.DateTimeFormat` API – no external dependencies.
- Outputs an emoji:
  - 🌅 sunrise (06‑11)
  - 🌞 daytime (12‑17)
  - 🌙 night (18‑05)
- Can be used as a CLI tool or imported as a library.

## Installation
```bash
# Clone the repository (or copy the utility folder) and install TypeScript globally if you don't have it
npm install -g typescript ts-node
```

## Usage
```bash
# Run directly with ts-node
npx ts-node src/index.ts America/New_York
```

Output example:
```
America/New_York 14:00 🌞
```

## API
```ts
import { getHourInTimezone, getEmojiForHour } from "./index";

const hour = getHourInTimezone("Europe/Paris"); // => number (0‑23)
const emoji = getEmojiForHour(hour); // => string
```

## Testing
```bash
npm test
```

The test suite uses Node's built‑in `assert` module and runs with `ts-node`.
