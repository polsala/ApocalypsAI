# nightly-collapse-chronicle

A whimsical TypeScript CLI that tells you how much time has passed since the Great Collapse (2023-01-01T00:00:00Z). Perfect for adding a post‑apocalyptic timestamp to logs, stories, or community events.

## Installation

```sh
npm install -g nightly-collapse-chronicle
```

## Usage

```sh
ncc [options] [date]
```

- If no date is provided, the current time is used.
- You can also pass an ISO‑8601 date string to calculate the elapsed time from that moment to the collapse.

### Options

- `-h, --help`   Show help

## Example

```sh
$ ncc
Days since the Great Collapse: 1023 days, 5 hours, 12 minutes, 30 seconds
```

## Development

```sh
npm install
npm run build
npm link   # makes `ncc` available globally
```

Run tests:

```sh
npm test
```
