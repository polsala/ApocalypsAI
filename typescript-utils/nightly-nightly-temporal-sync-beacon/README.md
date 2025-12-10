## Temporal Sync Beacon

In the chaotic aftermath, maintaining a consistent sense of time is crucial for coordination and survival. The Temporal Sync Beacon utility allows you to synchronize your local clock with a designated 'temporal beacon' server, ensuring that your timestamps are as accurate and aligned as possible with the rest of your community.

### Why?

*   **Event Ordering**: Crucial for reconstructing timelines of events, coordinating patrols, and managing resource distribution.
*   **Communication**: Ensures that messages and reports are timestamped consistently, reducing confusion.
*   **Resilience**: Provides a fallback for local clock drift or manual errors.

### Usage

1.  **Installation**:
    ```bash
    npm install @apocalypsai/temporal-sync-beacon
    ```
    or if building from source:
    ```bash
    git clone <repository_url>
    cd utils/nightly-temporal-sync-beacon
    npm install
    ```

2.  **Running the Utility**:
    The utility can be run as a command-line tool. It requires the URL of a temporal beacon server.

    ```bash
    npx @apocalypsai/temporal-sync-beacon --beacon-url <beacon_server_url> [--interval <seconds>]
    ```

    *   `--beacon-url`: The URL of the temporal beacon server (e.g., `http://beacon.wasteland.net/time`). **Required.**
    *   `--interval`: The interval in seconds at which to resynchronize. Defaults to 300 seconds (5 minutes).

3.  **As a Library**:
    You can also use this utility as a module in your own TypeScript or JavaScript projects.

    ```typescript
    import { TemporalSyncBeacon } from '@apocalypsai/temporal-sync-beacon';

    async function main() {
      const beaconUrl = 'http://beacon.wasteland.net/time';
      const syncInterval = 60; // Sync every 60 seconds

      const beacon = new TemporalSyncBeacon(beaconUrl, syncInterval);

      beacon.on('synced', (newTime: Date) => {
        console.log(`Time synchronized to: ${newTime.toISOString()}`);
      });

      beacon.on('error', (err: Error) => {
        console.error(`Synchronization error: ${err.message}`);
      });

      await beacon.start();
      console.log('Temporal Sync Beacon started.');

      // To stop:
      // beacon.stop();
    }

    main();
    ```

### Temporal Beacon Server Protocol

The temporal beacon server is expected to respond to GET requests at its root path (`/`) with a JSON object containing a single key `timestamp` whose value is the current server time in milliseconds since the Unix epoch.

Example Response:
```json
{
  "timestamp": 1678886400000
}
```

### Development & Testing

*   **Dependencies**: Node.js, npm/yarn
*   **Build**: `npm run build`
*   **Test**: `npm test`

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
