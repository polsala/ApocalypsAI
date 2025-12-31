## Nightly Temporal Sync Checker

A whimsical yet practical TypeScript utility designed to ensure the temporal integrity of event logs. In the chaotic aftermath of an apocalypse, maintaining a coherent timeline of events is crucial for survival and reconstruction. This tool helps by identifying and flagging any events that appear out of chronological order.

### Philosophy

"Order from chaos, one timestamp at a time." This utility embodies the principle of bringing order to the potentially jumbled streams of data that might arise in a post-apocalyptic world. It's built with type safety and clarity in mind, making it robust and easy to understand.

### Features

*   **Type-Safe Event Handling**: Utilizes TypeScript's strong typing to ensure event data is structured correctly.
*   **Chronological Verification**: Compares timestamps of sequential events to detect anomalies.
*   **Customizable Timestamp Format**: Supports flexible parsing of various timestamp formats.
*   **Clear Reporting**: Outputs a list of out-of-order events with relevant details.

### Installation

1.  Ensure you have Node.js and npm (or yarn/pnpm) installed.
2.  Clone this repository or download the utility files.
3.  Navigate to the utility's directory.
4.  Install dependencies:
    ```bash
    npm install
    ```

### Usage

The utility can be run from the command line. It expects a JSON array of event objects, where each object must have a `timestamp` field and an `id` field.

**Example Event Structure:**

```json
[
  { "id": "event-1", "timestamp": "2023-10-27T10:00:00Z", "data": "First contact" },
  { "id": "event-2", "timestamp": "2023-10-27T10:05:00Z", "data": "Resource found" },
  { "id": "event-3", "timestamp": "2023-10-27T10:03:00Z", "data": "Anomaly detected" } // Out of order!
]
```

**Running the checker:**

```bash
# Assuming your event log is in a file named 'events.json'
npx ts-node src/main.ts --file events.json
```

**Options:**

*   `--file <path>`: Path to the JSON file containing the event log.
*   `--format <format_string>`: Optional. A [date-fns format string](https://date-fns.org/v2.30.0/docs/format) to parse timestamps if they are not in ISO 8601 format. Defaults to ISO 8601.

### Development & Testing

This utility is built with TypeScript and includes unit tests using Jest. To run the tests:

```bash
npm test
```

### Contributing

Feel free to contribute by suggesting improvements, reporting bugs, or adding new features. All contributions are welcome!
