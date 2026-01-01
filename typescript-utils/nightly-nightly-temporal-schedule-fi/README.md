# nightly-temporal-schedule-fixer

A type-safe utility for the ApocalypsAI community to detect and suggest fixes for temporal paradoxes within task schedules. Ensure your post-apocalyptic plans are causally sound and free from spacetime distortions!

## Features

*   **Paradox Detection**: Identifies common scheduling anomalies:
    *   **Overlapping Tasks**: When two or more tasks attempt to occupy the same temporal slot.
    *   **Invalid Time Order**: Tasks that inexplicably end before they begin.
    *   **Zero/Negative Duration**: Tasks that exist for a fleeting moment or defy the laws of time.
    *   **Contained Tasks**: When one task is entirely engulfed by another, potentially indicating a sub-task or a scheduling oversight.
*   **Whimsical Suggestions**: Provides dramatic, apocalypse-themed suggestions for resolving detected paradoxes.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **Standalone CLI**: Can be run directly to analyze JSON schedule files.

## Installation

1.  Navigate to the `typescript-utils/nightly-temporal-schedule-fixer` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

### As a Library

YouYou can import and use the `detectTemporalParadoxes` function in your TypeScript/JavaScript projects:

```typescript
import { detectTemporalParadoxes, Task } from './src'; // Adjust path if installed as a package

const mySchedule: Task[] = [
  { id: "alpha", name: "Scavenge Sector 4", startTime: new Date("2024-07-20T09:00:00Z"), endTime: new Date("2024-07-20T11:00:00Z") },
  { id: "beta", name: "Repair Water Purifier", startTime: new Date("2024-07-20T10:30:00Z"), endTime: new Date("2024-07-20T12:00:00Z") }, // Overlap
  { id: "gamma", name: "Chronal Drift Calibration", startTime: new Date("2024-07-20T14:00:00Z"), endTime: new Date("2024-07-20T13:00:00Z") }, // Invalid order
];

const paradoxes = detectTemporalParadoxes(mySchedule);

if (paradoxes.length > 0) {
  console.log("Temporal anomalies detected in your schedule:");
  paradoxes.forEach(p => {
    console.log(`- Type: ${p.type}`);
    console.log(`  Message: ${p.message}`);
    if (p.suggestedFix) {
      console.log(`  Fix: ${p.suggestedFix}`);
    }
  });
} else {
  console.log("Your schedule is perfectly aligned with the spacetime continuum. Good job!");
}
```

### As a Command-Line Tool

1.  Build the project:
    ```bash
    npm run build
    ```
2.  Run the compiled script. Currently, the CLI example uses a hardcoded schedule. For a more robust CLI, you would extend `src/index.ts` to read a JSON file or stdin.

    ```bash
    node dist/index.js
    ```

    Expected output (based on the example schedule in `src/index.ts`):
    ```
    Nightly Temporal Schedule Fixer - CLI Mode
    Provide a JSON array of tasks to stdin, or implement file parsing.

    --- Detected Temporal Paradoxes ---

    Paradox 1:
      Type: OVERLAP
      Message: Temporal collision detected! Task 'Gather Scraps' (ID: 1) and 'Repair Drone' (ID: 2) occupy the same spacetime.
      Suggested Fix: Reschedule one of the tasks, 'Gather Scraps' or 'Repair Drone', to avoid temporal overlap. Perhaps a quantum shift in priorities?
      Involving Task A: 'Gather Scraps' (ID: 1) from 2024-04-20T10:00:00.000Z to 2024-04-20T11:00:00.000Z
      Involving Task B: 'Repair Drone' (ID: 2) from 2024-04-20T10:30:00.000Z to 2024-04-20T12:00:00.000Z

    Paradox 2:
      Type: INVALID_TIME_ORDER
      Message: Task 'Scout Sector 7' (ID: 3) defies causality: its end precedes its beginning!
      Suggested Fix: Adjust 'Scout Sector 7' to ensure startTime is before endTime. Perhaps a temporal realignment is in order?
      Involving Task A: 'Scout Sector 7' (ID: 3) from 2024-04-20T13:00:00.000Z to 2024-04-20T12:00:00.000Z

    Paradox 3:
      Type: NEGATIVE_DURATION
      Message: Task 'Meditate on Void' (ID: 4) exists in a single, fleeting moment. Is it truly a task, or a temporal echo?
      Suggested Fix: Extend the duration of 'Meditate on Void' or confirm it's an instantaneous event.
      Involving Task A: 'Meditate on Void' (ID: 4) from 2024-04-20T14:00:00.000Z to 2024-04-20T14:00:00.000Z

    Paradox 4:
      Type: CONTAINED_TASK
      Message: Task 'Check Anomaly Readings' (ID: 6) is entirely engulfed by 'Prepare for Anomaly' (ID: 5). A temporal black hole?
      Suggested Fix: Consider if 'Check Anomaly Readings' is a sub-task of 'Prepare for Anomaly' or if its timing needs to be adjusted to exist independently.
      Involving Task A: 'Prepare for Anomaly' (ID: 5) from 2024-04-20T15:00:00.000Z to 2024-04-20T17:00:00.000Z
      Involving Task B: 'Check Anomaly Readings' (ID: 6) from 2024-04-20T15:30:00.000Z to 2024-04-20T16:00:00.000Z
    ```

## Development

To run tests:
```bash
npm test
```

To compile TypeScript:
```bash
npm run build
```
