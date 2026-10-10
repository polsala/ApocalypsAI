# nightly-wasteland-calendar

Convert Gregorian dates to the post‑apocalypse Wasteland Calendar.

## Usage

```sh
npx nightly-wasteland-calendar 2025-04-01
# => Wasteland Year 2, Month 4, Day 1
```

## API

```ts
import { toWasteland } from "./src/index";

const wasteland = toWasteland("2025-04-01");
// "Year 2, Month 4, Day 1"
```

## Installation

```sh
npm install -g nightly-wasteland-calendar
```

## License

MIT
