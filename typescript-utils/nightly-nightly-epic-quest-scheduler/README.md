# nightly-epic-quest-scheduler

A whimsical CLI utility written in TypeScript that turns a list of adventure tasks into a dated fantasy quest itinerary.

## Installation

```sh
npm install -g ts-node
```

## Usage

```sh
ts-node src/questScheduler.ts <startDate> <task1> [task2 ...]
```

Example:

```sh
ts-node src/questScheduler.ts 2023-01-01 "Find the sword" "Defeat the dragon"
```

Will output markdown like:

```markdown
# Epic Quest Itinerary

## Day 1: 2023-01-01 – Mysterious Find the sword

## Day 2: 2023-01-02 – Radiant Defeat the dragon
```

## API

```ts
export function generateQuestSchedule(
  tasks: string[],
  startDate: string,
  randomFn?: () => number
): string;
```

- `tasks` – array of adventure task descriptions.
- `startDate` – ISO date string (e.g., `2023-01-01`).
- `randomFn` – optional deterministic random provider (defaults to `Math.random`).

## Testing

```sh
npm test
```

The test suite runs a deterministic check using a mocked random function.
