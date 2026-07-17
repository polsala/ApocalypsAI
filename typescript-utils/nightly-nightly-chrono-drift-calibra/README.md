# Nightly Chrono Drift Calibrator

A whimsical-yet-useful CLI tool for the ApocalypsAI community to help individuals (or AI agents!) recalibrate their internal sense of time against an objective standard. In a world of temporal anomalies, knowing how far off your internal clock is can be crucial for sanity, or at least for scheduling the next scavenging run.

This utility calculates the 'temporal drift' between a perceived time and an actual, objective time, then offers a fitting, whimsical 'recalibration mantra' to help you (or your circuits) re-synchronize.

## Features

*   **Type-Safe Time Handling**: Leverages TypeScript for robust date and time parsing and manipulation.
*   **Drift Calculation**: Precisely measures the difference in milliseconds between two timestamps.
*   **Whimsical Mantras**: Provides context-sensitive, encouraging (or alarming) messages based on the severity of the temporal drift.
*   **CLI Interface**: Easy to use from the command line.

## Installation

1.  Ensure you have Node.js (v18 or higher recommended) and npm (or yarn) installed.
2.  Navigate to the `nightly-chrono-drift-calibrator` directory.
3.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## Usage

Run the calibrator from your terminal, providing the actual time and your perceived time as ISO 8601 strings.

```bash
node dist/index.js <actual_time_iso> <perceived_time_iso>
```

### Arguments

*   `<actual_time_iso>`: The objective, correct time in ISO 8601 format (e.g., `2023-10-27T10:00:00.000Z`).
*   `<perceived_time_iso>`: Your perceived time in ISO 8601 format.

### Examples

*   **Perfect Alignment**:
    ```bash
    node dist/index.js "2023-10-27T10:00:00.000Z" "2023-10-27T10:00:00.000Z"
    ```
    Output:
    ```
    Temporal Drift: 0ms
    Recalibration Mantra: Your internal chronometer is perfectly aligned with the cosmic flow. Serenity.
    ```

*   **Slight Drift (10 seconds ahead)**:
    ```bash
    node dist/index.js "2023-10-27T10:00:00.000Z" "2023-10-27T10:00:10.000Z"
    ```
    Output:
    ```
    Temporal Drift: 10000ms
    Recalibration Mantra: A gentle nudge for your temporal compass. Breathe and realign.
    ```

*   **Significant Drift (2 hours behind)**:
    ```bash
    node dist/index.js "2023-10-27T12:00:00.000Z" "2023-10-27T10:00:00.000Z"
    ```
    Output:
    ```
    Temporal Drift: -7200000ms
    Recalibration Mantra: Significant temporal resonance detected. Seek a stable temporal anchor.
    ```

## Development

To run tests:

```bash
npm test
```
