# Nightly Chrono-Shift Calculator

The **Nightly Chrono-Shift Calculator** is a whimsical-yet-useful utility designed to help you navigate the temporal currents of the apocalypse (or just your busy schedule). It allows you to calculate future dates and times by applying a series of defined temporal shifts, making complex scheduling and event planning a breeze.

Whether you need to figure out the next available business day after a series of tasks, or pinpoint the exact time a temporal anomaly will manifest after several "add day" and "skip weekend" adjustments, this tool has you covered.

## Features

*   **Flexible Date Manipulation**: Add or subtract years, months, weeks, days, hours, minutes, or seconds.
*   **Precise Time Setting**: Set specific hours, minutes, and seconds for a given date.
*   **Weekend Skipping**: Automatically adjust dates to the next Monday if they fall on a Saturday or Sunday.
*   **Next Weekday Finder**: Easily find the next occurrence of a specific day of the week (e.g., next Tuesday), including the current day if it matches.
*   **Type-Safe**: Built with TypeScript for robust and predictable date calculations.

## Installation

To use this utility, you'll need Node.js (v14 or higher) and npm/yarn installed.

1.  Navigate to the `nightly-chrono-shift-calc` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

The utility can be used as a command-line tool.

```bash
npm start -- --start-date "YYYY-MM-DDTHH:mm:ss" --shifts '[{"type":"add","unit":"days","value":7},{"type":"skip-weekends"},{"type":"set-time","hour":9,"minute":0,"second":0}]'
```

### Command-Line Arguments

*   `--start-date <date-string>`: The initial date and time from which to apply shifts. Must be a valid ISO 8601 date string (e.g., "2023-10-26T10:00:00").
*   `--shifts <json-array-string>`: A JSON string representing an array of temporal shifts to apply.

### Shift Types

Here are the available shift types and their parameters:

1.  **`add` / `subtract`**: Adds or subtracts a specified value from a time unit.
    *   `type`: `"add"` or `"subtract"`
    *   `unit`: `"years"`, `"months"`, `"weeks"`, `"days"`, `"hours"`, `"minutes"`, `"seconds"`
    *   `value`: `number` (e.g., `1`, `5`, `-2`)
    *   Example: `{"type": "add", "unit": "days", "value": 3}`

2.  **`set-time`**: Sets the hour, minute, and second of the date.
    *   `type`: `"set-time"`
    *   `hour`: `number` (0-23)
    *   `minute`: `number` (0-59)
    *   `second`: `number` (0-59)
    *   Example: `{"type": "set-time", "hour": 9, "minute": 30, "second": 0}`

3.  **`skip-weekends`**: If the date falls on a Saturday or Sunday, it shifts it to the next Monday. Note that `date-fns`' `nextMonday` function, used internally, will reset the time to `00:00:00` on the new Monday.
    *   `type`: `"skip-weekends"`
    *   Example: `{"type": "skip-weekends"}`

4.  **`find-next-weekday`**: Finds the next occurrence of a specific day of the week, including the current day if it matches.
    *   `type`: `"find-next-weekday"`
    *   `weekday`: `number` (0 for Sunday, 1 for Monday, ..., 6 for Saturday)
    *   Example: `{"type": "find-next-weekday", "weekday": 5}` (find next Friday)

## Examples

### Example 1: Add days and skip weekends
Start on a Friday, add 2 days, then skip weekends.
```bash
# Start: Friday, Oct 27, 2023, 10:00:00 UTC
# Add 2 days -> Sunday, Oct 29, 2023, 10:00:00 UTC
# Skip weekends -> Monday, Oct 30, 2023, 00:00:00 UTC (time reset by nextMonday)
npm start -- --start-date "2023-10-27T10:00:00Z" --shifts '[{"type":"add","unit":"days","value":2},{"type":"skip-weekends"}]'
# Expected Output: 2023-10-30T00:00:00.000Z
```

### Example 2: Set time and find next Tuesday
Start on a Monday, set time to 14:00, then find next Tuesday.
```bash
# Start: Monday, Oct 23, 2023, 10:00:00 UTC
# Set time -> Monday, Oct 23, 2023, 14:00:00 UTC
# Find next Tuesday (weekday 2) -> Tuesday, Oct 24, 2023, 14:00:00 UTC
npm start -- --start-date "2023-10-23T10:00:00Z" --shifts '[{"type":"set-time","hour":14,"minute":0,"second":0},{"type":"find-next-weekday","weekday":2}]'
# Expected Output: 2023-10-24T14:00:00.000Z
```

## Development

### Running Tests

```bash
npm test
```

### Building

```bash
npm run build
```
