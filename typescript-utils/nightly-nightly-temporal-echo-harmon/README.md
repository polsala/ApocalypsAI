# Nightly Temporal Echo Harmonizer

The `nightly-temporal-echo-harmonizer` is a whimsical-yet-useful utility designed to bring order to the chaotic stream of "temporal echoes" – fragmented, time-stamped messages or data points. In a world of temporal distortions and information overload, this tool helps piece together coherent narratives and understand the underlying sentiment of events by grouping related echoes based on their temporal proximity.

## Features

*   **Temporal Grouping:** Automatically groups echoes into "narratives" if their timestamps fall within a configurable time threshold.
*   **Sentiment Analysis:** Provides a basic sentiment (positive, negative, neutral, mixed) for each harmonized narrative, based on a set of predefined keywords.
*   **Narrative Summarization:** Generates a concise summary for each identified narrative.
*   **Type-Safe:** Built with TypeScript for robust and predictable data handling.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd typescript-utils/nightly-temporal-echo-harmonizer
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

The utility can be run directly using `ts-node` or after building with `npm run build` and then `node`.

### Command Line Interface (CLI)

The CLI expects a time threshold in minutes, followed by pairs of timestamp strings and message strings.

```bash
npm start <timeThresholdMinutes> <echo1_timestamp> <echo1_message> [<echo2_timestamp> <echo2_message> ...]
```

**Example:**

```bash
npm start 5 "2023-01-01T10:00:00Z" "Found a cache of supplies, all good!" "2023-01-01T10:02:30Z" "Area clear, no immediate danger." "2023-01-01T10:15:00Z" "New signal detected, origin unknown."
```

This will output a JSON array of harmonized narratives:

```json
[
  {
    "id": "narrative-1",
    "echoes": [
      {
        "id": "echo-1",
        "timestamp": "2023-01-01T10:00:00.000Z",
        "message": "Found a cache of supplies, all good!"
      },
      {
        "id": "echo-2",
        "timestamp": "2023-01-01T10:02:30.000Z",
        "message": "Area clear, no immediate danger."
      }
    ],
    "summary": "Sequence of 2 echoes: \"Found a cache of supplies, all good!; Area clear, no immediate danger.\"",
    "sentiment": "positive",
    "temporalSpanMs": 150000
  },
  {
    "id": "narrative-2",
    "echoes": [
      {
        "id": "echo-3",
        "timestamp": "2023-01-01T10:15:00.000Z",
        "message": "New signal detected, origin unknown."
      }
    ],
    "summary": "Single echo: \"New signal detected, origin unknown.\"",
    "sentiment": "neutral",
    "temporalSpanMs": 0
  }
]
```

### As a Library

You can also import and use the `TemporalEchoHarmonizer` class in your own TypeScript/JavaScript projects:

```typescript
import { TemporalEchoHarmonizer, TemporalEcho } from 'nightly-temporal-echo-harmonizer';

const harmonizer = new TemporalEchoHarmonizer(10); // 10 minutes threshold

const echoes: TemporalEcho[] = [
  { id: 'a1', timestamp: new Date('2023-03-15T08:00:00Z'), message: 'Sensor reading: stable.' },
  { id: 'a2', timestamp: new Date('2023-03-15T08:03:00Z'), message: 'Communication log: "All clear."' },
  { id: 'b1', timestamp: new Date('2023-03-15T09:30:00Z'), message: 'Anomaly detected! Danger!' },
  { id: 'b2', timestamp: new Date('2023-03-15T09:31:00Z'), message: 'System integrity compromised.' },
];

const narratives = harmonizer.harmonize(echoes);
console.log(JSON.stringify(narratives, null, 2));
```

## Development

### Building

```bash
npm run build
```

This will compile the TypeScript code into JavaScript in the `dist/` directory.

### Testing

```bash
npm test
```

This will run the Jest test suite, ensuring the harmonizer logic works as expected. Tests are deterministic and use mocked data for timestamps and sentiment analysis.

## Contributing

Feel free to contribute to the Temporal Echo Harmonizer! Ideas for improvement include:
*   More sophisticated sentiment analysis (e.g., using an external library or API).
*   Advanced summarization techniques.
*   Support for different input formats (e.g., CSV, JSON files).
*   Configurable keyword sets for sentiment analysis.
