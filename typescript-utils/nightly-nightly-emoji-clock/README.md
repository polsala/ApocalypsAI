# nightly-emoji-clock

A tiny TypeScript utility that converts a 24‑hour time string (HH:MM) into the closest clock‑face emoji. Perfect for adding whimsical timestamps to chat messages, commit logs, or any text where a visual cue is welcome.

## Installation

```sh
npm install -g ts-node
git clone <repo> && cd utils/nightly-emoji-clock
npm install
```

(Or simply run the script with `npx ts-node src/cli.ts`.)

## Usage

```sh
npx ts-node src/cli.ts 14:45
🕓
```

The tool rounds to the nearest hour or half‑hour emoji.

## API

```ts
timeToClockEmoji(time: string): string
```

- `time` – a string in `HH:MM` 24‑hour format.
- Returns the corresponding clock emoji.

Throws an error on invalid input.

## Testing

```sh
npm test
```

Runs the bundled TypeScript tests with Node's built‑in assert module.
