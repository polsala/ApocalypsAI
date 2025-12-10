# Temporal Sync Beacon

A whimsical yet practical TypeScript utility designed to synchronize your local system's time with a designated 'temporal beacon'. This is particularly useful in distributed systems or when coordinating events across different machines where precise, consistent timing is crucial, even in the face of temporal distortions.

## Features

*   **Beacon Synchronization**: Connects to a specified temporal beacon URL to fetch its current time.
*   **Local Time Adjustment**: Calculates the offset between local and beacon time and provides a mechanism to 'nudge' local time.
*   **Type-Safe**: Built with TypeScript for robust type checking and developer experience.
*   **Offline Testing**: Includes deterministic tests with mocked network requests.

## Installation

```bash
npm install @apocalypsai/temporal-sync-beacon
# or
yarn add @apocalypsai/temporal-sync-beacon
```

## Usage

### CLI (Example)

This utility can be run as a command-line tool. Assuming you have it installed globally or via `npx`:

```bash
npx @apocalypsai/temporal-sync-beacon --beacon-url http://example.com/temporal-beacon --interval 60000
```

*   `--beacon-url`: The URL of the temporal beacon (defaults to a mock beacon).
*   `--interval`: The synchronization interval in milliseconds (defaults to 60000ms / 1 minute).

### Programmatic Usage

```typescript
import { TemporalSyncBeacon } from '@apocalypsai/temporal-sync-beacon';

async function main() {
  const beaconUrl = 'http://your-temporal-beacon.com/api/time';
  const syncInterval = 30000; // 30 seconds

  const beacon = new TemporalSyncBeacon(beaconUrl, syncInterval);

  beacon.on('synced', (offsetMs: number) => {
    console.log(`Time synchronized. Offset: ${offsetMs}ms`);
  });

  beacon.on('error', (err: Error) => {
    console.error(`Synchronization error: ${err.message}`);
  });

  console.log('Starting temporal synchronization...');
  await beacon.start();

  // To stop synchronization later:
  // beacon.stop();
}

main().catch(console.error);
```

## Temporal Beacon Protocol

The temporal beacon is expected to respond to GET requests with a JSON payload containing a `timestamp` field, representing the beacon's current time in milliseconds since the Unix epoch.

Example Beacon Response:

```json
{
  "timestamp": 1678886400000
}
```

## Development & Testing

This project uses Jest for testing. All tests are deterministic and do not require external network access.

```bash
npm install
npm test
```
