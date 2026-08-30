# Nightly Chrono-Drift Adjuster

A whimsical-yet-useful Node.js CLI tool designed to help you synchronize your internal clock with the ever-shifting temporal fabric of the cosmos. Or, at least, a simulated version of it.

In a world where time itself might be a suggestion, the Chrono-Drift Adjuster provides a recommended adjustment to your local time, based on a pseudo-random 'cosmic drift' calculation. It's perfect for those who suspect their watches are subtly out of sync with the universe, or just want a fun, deterministic way to introduce a little temporal chaos.

## Features

*   **Simulated Temporal Drift**: Calculates a positive, negative, or zero second adjustment based on a daily-changing (or user-defined) seed.
*   **Temporal Stability Forecast**: Provides a whimsical message indicating the perceived stability of the temporal fabric.
*   **Cross-Platform**: Runs anywhere Node.js is supported.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Navigate to the utility directory**:
    ```bash
    cd nightly-chrono-drift-adjuster
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the adjuster from your terminal:

```bash
node src/index.js
# Or, if you've added it to your PATH or linked it:
# chrono-drift-adjuster
```

### Options

*   `-s, --seed <number>`: Provide a numerical seed for the drift calculation. This allows you to get a consistent drift result for a specific 'day' or 'event'. If not provided, the tool uses the current day (days since epoch) as the seed.

    Example:
    ```bash
    node src/index.js --seed 42
    ```

## Example Output

```
--- Nightly Chrono-Drift Adjuster ---
Current Local Time: 10:30:45 AM
Temporal Seed Used: 19649
Detected Chrono-Drift: +3 seconds
Recommended Adjustment: ADD 3 seconds
Calibrated Local Time (approx): 10:30:48 AM

Temporal Stability Forecast: Minor temporal ripples detected. A slight recalibration is advised.
-------------------------------------
```

## How it Works (The Whimsical Math)

The 'chrono-drift' is calculated using a simple formula based on the provided or derived seed:

1.  `driftMagnitude = (seed % 13) - 6` (results in a value between -6 and +6)
2.  `driftDirection = (seed % 2 === 0) ? 1 : -1` (alternates positive/negative)
3.  `adjustmentSeconds = driftMagnitude * driftDirection`

This ensures a deterministic, yet seemingly random, adjustment that changes daily (or with your chosen seed).

## Development

### Running Tests

To ensure the temporal calculations are consistent, run the automated tests:

```bash
npm test
```
