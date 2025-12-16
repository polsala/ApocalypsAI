## Temporal Sync Beacon

A whimsical yet practical TypeScript utility designed to synchronize your local system's time with a designated remote 'beacon' server. In the chaotic aftermath of the apocalypse, maintaining temporal consistency is crucial for coordinated efforts. This tool helps ensure your clocks are aligned, preventing temporal paradoxes and facilitating smoother operations.

### Features

*   **Beacon Synchronization**: Connects to a specified beacon URL to fetch its current time.
*   **Local Time Adjustment**: Calculates the offset and suggests or applies adjustments to the local system time (requires appropriate permissions).
*   **Configurable Beacon**: Easily set the beacon URL via command-line arguments or environment variables.
*   **Human-Readable Output**: Provides clear feedback on the synchronization process and any detected discrepancies.

### Installation

1.  **Prerequisites**: Node.js and npm/yarn installed.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility**: `cd ApocalypsAI/utils/nightly-temporal-sync-beacon`
4.  **Install dependencies**: `npm install` or `yarn install`

### Usage

Run the utility from your terminal:

```bash
npx ts-node src/main.ts --beacon-url <beacon_url>
```

**Example**: 

```bash
npx ts-node src/main.ts --beacon-url http://apoc-time-beacon.example.com/time
```

**Options**:

*   `--beacon-url <url>`: The URL of the temporal beacon to synchronize with. (Required)
*   `--adjust`: If provided, the utility will attempt to adjust the local system time. (Requires elevated privileges)

### How it Works

The utility makes an HTTP GET request to the specified beacon URL. The beacon is expected to respond with a JSON object containing a `timestamp` field (in milliseconds since the Unix epoch). The utility then compares this timestamp with its local system time, calculates the difference, and reports it. If the `--adjust` flag is used, it will attempt to use system commands to set the local time.

### Testing

Automated tests are included to verify the functionality. Run them using:

```bash
npm test
```

### Contributing

Contributions are welcome! Please follow the ApocalypsAI contribution guidelines.
