# nightly-solar-flare-countdown

A whimsical Node.js CLI that tells you how many days remain until the next scheduled solar flare (fictional). Useful for post‑apocalyptic role‑playing or just for fun.

## Installation

```sh
npm install -g nightly-solar-flare-countdown
```

or run via npx:

```sh
npx nightly-solar-flare-countdown
```

## Usage

```sh
nightly-solar-flare-countdown [date]
```

- `date` (optional) – a date string parseable by `new Date()`. If omitted, the current system date is used.

The tool prints the number of days until the next flare. If the given date is after the last known flare, it reports that no upcoming flares are scheduled.

## Example

```sh
$ nightly-solar-flare-countdown 2024-08-01
Days until next solar flare: 45
```

## How it works

The utility contains a hard‑coded list of fictional future solar flare dates. It finds the first date after the supplied/current date and calculates the difference in whole days.
