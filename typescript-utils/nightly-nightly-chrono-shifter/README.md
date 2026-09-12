# Nightly Chrono-Shifter

A whimsical-yet-useful TypeScript CLI tool that allows you to shift a given date by non-standard, fantastical temporal units. Ever wondered what your deadline would be after a 'lunar cycle' or a 'void whisper'? Now you can find out!

## Features

*   **Whimsical Temporal Units**: Shift dates by 'lunar-cycle', 'void-whisper', 'temporal-ripple', 'stardust-blink', and 'cosmic-tide'.
*   **Type-Safe**: Built with TypeScript for robust input validation and predictable date manipulation.
*   **CLI Interface**: Easily integrate into scripts or use directly from your terminal.

## Installation

1.  Navigate to the `typescript-utils/nightly-chrono-shifter` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the utility from the command line, providing a date string and a shift unit.

```bash
node dist/index.js <date-string> <shift-unit>
```

**Arguments:**

*   `<date-string>`: The starting date and time in ISO 8601 format (e.g., `2023-10-27T10:00:00Z`).
*   `<shift-unit>`: One of the following whimsical temporal units:
    *   `lunar-cycle`: Approximately 29 days and 12 hours.
    *   `void-whisper`: 7 hours, 7 minutes, 7 seconds.
    *   `temporal-ripple`: 13 days, 13 hours.
    *   `stardust-blink`: 1 minute, 1 second.
    *   `cosmic-tide`: Approximately 182 days.

**Examples:**

Shift a date by a lunar cycle:
```bash
npm start -- '2023-10-27T10:00:00Z' 'lunar-cycle'
# Expected Output:
# Original Date: 2023-10-27T10:00:00.000Z
# Shift Unit: lunar-cycle
# Shifted Date: 2023-11-25T22:00:00.000Z
# Description: Your date has been shifted forward by one ethereal lunar cycle.
```

Shift a date by a void whisper:
```bash
npm start -- '2024-01-01T00:00:00Z' 'void-whisper'
```

## Development

### Running Tests

To ensure the date shifting logic works as expected, run the automated tests:

```bash
npm test
```

### Project Structure

```
.gitignore
package.json
tsconfig.json
jest.config.js
src/
  chronoShifter.ts  # Core date shifting logic and types
  index.ts           # CLI entry point
tests/
  chronoShifter.test.ts # Unit tests for chronoShifter.ts
```
