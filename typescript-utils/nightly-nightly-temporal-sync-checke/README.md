# Nightly Temporal Sync Checker

A whimsical yet practical TypeScript utility designed to ensure the temporal integrity of event logs. In the chaotic aftermath of an apocalypse, maintaining a coherent timeline of events is crucial for survival and reconstruction. This tool helps by verifying that events in a log are chronologically ordered.

## Features

*   **Type-Safe Event Handling**: Utilizes TypeScript for robust type checking of event structures.
*   **Chronological Verification**: Checks if event timestamps are monotonically increasing.
*   **Customizable Timestamp Field**: Allows specifying which field in an event object represents the timestamp.
*   **Error Reporting**: Provides clear messages for out-of-order events.

## Installation

```bash
npm install --save-dev @types/node
```

## Usage

1.  **Define your Event Type**: Create an interface or type for your events, ensuring it has a timestamp property.

    ```typescript
    interface ApocalypseEvent {
      id: string;
      type: string;
      timestamp: number; // Unix timestamp in milliseconds
      payload: any;
    }
    ```

2.  **Create a Log**: Prepare an array of your event objects.

    ```typescript
    const eventLog: ApocalypseEvent[] = [
      { id: 'e1', type: 'scavenge', timestamp: 1678886400000, payload: { item: 'canned_beans' } },
      { id: 'e2', type: 'repair', timestamp: 1678886460000, payload: { device: 'water_purifier' } },
      { id: 'e3', type: 'scavenge', timestamp: 1678886520000, payload: { item: 'medkit' } },
      // ... more events
    ];
    ```

3.  **Run the Checker**: Instantiate `TemporalSyncChecker` and call the `checkLog` method.

    ```typescript
    import { TemporalSyncChecker } from './src/temporalSyncChecker';

    const checker = new TemporalSyncChecker<ApocalypseEvent>('timestamp');
    const inconsistencies = checker.checkLog(eventLog);

    if (inconsistencies.length > 0) {
      console.error('Temporal inconsistencies found:');
      inconsistencies.forEach(inc => console.error(`- Event ${inc.event.id} at index ${inc.index} has timestamp ${inc.event.timestamp} which is earlier than previous event.`));
    } else {
      console.log('Event log is temporally consistent!');
    }
    ```

## API

### `TemporalSyncChecker<T extends { [key: string]: any }>`

*   **Constructor**: `constructor(timestampField: keyof T)`
    *   Initializes the checker with the name of the field to use for timestamps.

*   **`checkLog(log: T[]): TemporalInconsistency<T>[]`**
    *   Takes an array of event objects (`log`).
    *   Returns an array of `TemporalInconsistency` objects, detailing any out-of-order events.

### `TemporalInconsistency<T>`

*   `event: T`: The event that is out of order.
*   `index: number`: The index of the out-of-order event in the log.
*   `previousTimestamp: number`: The timestamp of the preceding event.

## Development & Testing

This utility is built with TypeScript and includes unit tests using Node.js's built-in `assert` module. You can run the tests using:

```bash
npx ts-node tests/test_temporalSyncChecker.ts
```
