# Nightly Temporal Scrap Parser

Parses and normalizes inconsistent date/time strings from scavenged data, providing a confidence score for reliability. In the post-apocalyptic landscape, data comes in all forms – from hastily scribbled notes to corrupted digital logs. This utility helps make sense of the temporal chaos by attempting to parse various date formats and indicating how confident it is in the result.

## Features

*   **Multi-format Parsing**: Attempts to parse a wide range of date and time formats.
*   **Confidence Scoring**: Assigns 'High', 'Medium', 'Low', or 'None' confidence to parsed dates based on format explicitness and ambiguity.
*   **Type-Safe Output**: Returns a structured object with the original string, parsed `Date` object (if successful), and confidence level.
*   **CLI Interface**: Easily parse date strings directly from your terminal.

## Installation

1.  Navigate to the `typescript-utils/nightly-temporal-scrap-parser` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

### Command Line Interface (CLI)

Run the utility directly from your terminal:

```bash
npm start "2023-10-27T14:30:00Z"
# Output:
# Original: "2023-10-27T14:30:00Z"
# Parsed: 2023-10-27T14:30:00.000Z
# Confidence: High

npm start "Oct 27, 2023 10:00 AM"
# Output:
# Original: "Oct 27, 2023 10:00 AM"
# Parsed: 2023-10-27T14:00:00.000Z (Note: Timezone conversion might occur based on system)
# Confidence: Medium

npm start "12/31/22"
# Output:
# Original: "12/31/22"
# Parsed: 2022-12-31T00:00:00.000Z
# Confidence: Medium

npm start "27 Oct 2023"
# Output:
# Original: "27 Oct 2023"
# Parsed: 2023-10-27T00:00:00.000Z
# Confidence: Low

npm start "yesterday's log"
# Output:
# Original: "yesterday's log"
# Parsed: N/A
# Confidence: None
# Error: Could not parse date string.
```

### As a Module

You can also import and use the `parseScrapedDate` function in your own TypeScript/JavaScript projects:

```typescript
import { parseScrapedDate, ScrapedDate } from '../dist/index'; // Adjust path as needed

const result1: ScrapedDate = parseScrapedDate('2023-01-01 12:00:00');
console.log(result1);
// { original: '2023-01-01 12:00:00', parsed: Date object, confidence: 'High' }

const result2: ScrapedDate = parseScrapedDate('01/01/2023');
console.log(result2);
// { original: '01/01/2023', parsed: Date object, confidence: 'Medium' }

const result3: ScrapedDate = parseScrapedDate('random text');
console.log(result3);
// { original: 'random text', parsed: null, confidence: 'None', error: 'Could not parse date string.' }
```

## Development

### Running Tests

To ensure everything is working as expected, run the test suite:

```bash
npm test
```

Tests are deterministic and offline, using mocks for `console.log` and `console.error` during CLI tests. The `Date` object's parsing behavior for absolute dates is considered deterministic for the purpose of these tests, with specific handling for local vs. UTC interpretations.

## Contributing

Feel free to scavenge for improvements! If you find a date format that isn't handled well or have ideas for improving confidence scoring, contributions are welcome.
