# nightly-emoji-chronometer

A whimsical TypeScript CLI that visualizes the passage of time using moon phase emojis. Useful for adding fun progress indicators to scripts.

## Installation

```sh
npm install -g .
```

## Usage

```sh
npx nightly-emoji-chronometer 10 --interval 2
```

The above command will output a moon emoji every 2 seconds for a total of 10 seconds.

## API

```ts
export function generateChrono(seconds: number, interval?: number): string[]
```

Returns an array of moon‑phase emojis representing each tick.

