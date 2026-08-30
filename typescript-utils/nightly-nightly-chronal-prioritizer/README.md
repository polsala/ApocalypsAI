# Nightly Chronal Prioritizer

A type-safe CLI tool to prioritize tasks based on urgency, importance, and a touch of temporal whimsy.

## Overview

In the chaotic aftermath, effective task prioritization is paramount. The `Nightly Chronal Prioritizer` helps you sort through your daily duties, not just by mundane metrics like urgency and importance, but also by a "whimsy factor" that introduces a delightful, albeit slight, temporal distortion into the prioritization algorithm. This ensures that while critical tasks rise to the top, the universe's inherent unpredictability (and perhaps a hint of cosmic humor) is also accounted for.

This utility is built with TypeScript, offering robust type safety and a clear, maintainable codebase.

## Features

*   **Type-Safe Task Definition**: Define tasks with clear `name`, `urgency`, `importance`, and an optional `whimsyFactor`.
*   **Configurable Prioritization**: Weights for urgency, importance, and whimsy can be adjusted (in `src/index.ts`).
*   **Temporal Whimsy**: A subtle, randomized "temporal distortion" factor is applied to the whimsy component, making each prioritization run uniquely aligned with the cosmic flow (mocked for deterministic testing).
*   **CLI Ready**: Run directly from your terminal to get an instant prioritized list.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd nightly-chronal-prioritizer
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Build the TypeScript project**:
    ```bash
    npm run build
    ```

## Usage

To run the prioritizer with example tasks:

```bash
npm start
```

This will output a list of example tasks, first unprioritized, then chronally prioritized with their calculated scores.

### Defining Your Own Tasks

You can modify the `exampleTasks` array in `src/index.ts` to prioritize your own list of tasks.

Each task should conform to the `Task` interface:

```typescript
interface Task {
  name: string;
  urgency: number; // A number from 1 (low) to 5 (high)
  importance: number; // A number from 1 (low) to 5 (high)
  whimsyFactor?: number; // An optional number from 0 (no whimsy) to 1 (maximum whimsy)
}
```

**Example:**

```typescript
const myTasks: Task[] = [
  { name: 'Repair Flux Capacitor', urgency: 5, importance: 5, whimsyFactor: 0.2 },
  { name: 'Feed the Chrono-Hamster', urgency: 3, importance: 4, whimsyFactor: 0.9 },
  { name: 'Decipher Ancient Time Scrolls', urgency: 4, importance: 3 }, // whimsyFactor defaults to 0.5
];
```

## Development

### Running Tests

To ensure the chronal integrity of the prioritizer, run the tests:

```bash
npm test
```

Tests are deterministic thanks to mocking `Math.random()`, ensuring consistent results across runs.

### Project Structure

```
.
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts        # Main logic and CLI entry point
│   └── task.ts         # Task interface definitions
└── tests/
    └── index.test.ts   # Unit tests for prioritization logic
```

## License

This project is licensed under the MIT License.
