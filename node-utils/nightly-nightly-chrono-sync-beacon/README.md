# Nightly Chrono-Sync Beacon

In the chaotic temporal landscape of the post-apocalypse, precise time synchronization is a luxury. The `nightly-chrono-sync-beacon` is a simple, yet vital, utility designed to emit a reliable temporal signal: a current ISO timestamp paired with an optional 'temporal signature' (a SHA256 hash). This beacon can be used by disparate systems to establish a common temporal reference point, aiding in log correlation, event ordering, and general sanity maintenance.

## Features

*   **Precise Timestamp**: Outputs the current time in ISO 8601 format.
*   **Temporal Signature**: Generates a SHA256 hash based on the timestamp and an optional user-provided context string, ensuring a unique and verifiable beacon.
*   **Machine-Readable Output**: Provides output in JSON format for easy integration into other scripts and systems.

## Installation

1.  Navigate to the `node-utils/nightly-chrono-sync-beacon` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js [options]
```

### Options

*   `-c, --context <string>`: An optional string to include in the temporal signature hash. Useful for embedding system identifiers, event types, or other relevant data.

### Examples

#### Basic Beacon

```bash
node src/index.js
```

Example Output:

```json
{
  "timestamp": "2023-10-27T10:30:00.123Z",
  "signature": "a1b2c3d4e5f67890..."
}
```

#### Beacon with Context

```bash
node src/index.js --context "SectorAlpha-LogProcessor-001"
```

Example Output:

```json
{
  "timestamp": "2023-10-27T10:30:00.123Z",
  "context": "SectorAlpha-LogProcessor-001",
  "signature": "f0e9d8c7b6a54321..."
}
```

## Development

### Running Tests

```bash
npm test
```
