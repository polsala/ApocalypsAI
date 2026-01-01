# nightly-emoji-calendar

A whimsical yet useful CLI tool that prints a monthly calendar with emojis representing each day of the week.

## Features

- Generates a calendar for any month and year.
- Each day of the week is represented by a distinct emoji.
- Works as a Node.js script or as a library.

## Usage

```bash
# Install dependencies
npm install

# Run the CLI for the current month
node src/main.ts

# Run the CLI for a specific month
node src/main.ts 2023 12
```

## As a library

```ts
import { generateCalendar } from './src/main';

const calendar = generateCalendar(2023, 12);
console.log(calendar);
```

## License

MIT
