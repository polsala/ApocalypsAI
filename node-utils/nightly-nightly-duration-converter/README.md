# nightly-duration-converter

Convert between humanâreadable duration strings (e.g., `2h30m15s`) and total seconds.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js parse 2h30m   # => 9000
node src/index.js format 9000   # => 2h 30m
```

## API

- `parseDuration(str): number` â returns total seconds.
- `formatDuration(seconds): string` â returns formatted string.

## Tests

```sh
node tests/test_index.js
```
