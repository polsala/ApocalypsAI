# nightly-wasteland-calendar

Convert Gregorian dates to the whimsical post‑apocalyptic Wasteland Calendar.

## Installation

```sh
npm install -D typescript ts-node
```

## Usage

```sh
npx ts-node src/index.ts 2025-04-01
# => 25-Scorch-01
```

## API

```ts
import { convert } from "./index";

const wc = convert("2025-04-01"); // "25-Scorch-01"
```

The calendar has 13 months of 28 days each, named:

- Ash
- Dust
- Ruin
- Scorch
- Blight
- Cinder
- Gloom
- Ember
- Frost
- Shade
- Dusk
- Night
- Eclipse

The year is calculated as Gregorian year minus 2000. Dates before 2000 return `"Pre‑Apocalypse"`.
