# Nightly Apocalypse Calendar

A whimsical CLI utility that tells you how many days have passed since the Great Fallout (January 1, 2023). Useful for tracking postâapocalyptic time in scripts or just for fun.

## Installation

```sh
npm install -g nightly-apocalypse-calendar
```

## Usage

```sh
npx nightly-apocalypse-calendar          # uses today
npx nightly-apocalypse-calendar 2023-02-01
```

Outputs: `It has been 31 days since the Great Fallout.`

## API

```ts
import { computeDays } from "nightly-apocalypse-calendar";

const days = computeDays(new Date("2023-02-01"));
```

## License

MIT
