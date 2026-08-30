# Nightly Chrono-Compass

A whimsical-yet-useful CLI tool for survivors to orient themselves in a world where traditional timekeeping might be... less reliable. The Chrono-Compass calculates the time until the next sunrise and sunset for a given location, and can also track time relative to a custom "event" timestamp.

## Features

*   **Dawn/Dusk Tracking**: Get precise times for the next sunrise and sunset based on latitude and longitude.
*   **Event Tracking**: Calculate time elapsed since or remaining until a specific custom event.
*   **Cross-Platform**: Built with Node.js, runs anywhere Node.js is supported.

## Installation

1.  Ensure Node.js is installed (v14 or higher recommended).
2.  Clone the repository or download the `nightly-chrono-compass` folder.
3.  Navigate into the `nightly-chrono-compass` directory:
    ```bash
    cd nightly-chrono-compass
    ```
4.  Install dependencies (Jest for testing):
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js --lat <latitude> --lon <longitude> [--date <YYYY-MM-DD>] [--event <YYYY-MM-DDTHH:MM:SSZ>]
```

### Arguments:

*   `--lat <latitude>`: (Required) The latitude of your current location (e.g., `34.0522`).
*   `--lon <longitude>`: (Required) The longitude of your current location (e.g., `-118.2437`).
*   `--date <YYYY-MM-DD>`: (Optional) The date for which to calculate sunrise/sunset. Defaults to the current system date.
*   `--event <YYYY-MM-DDTHH:MM:SSZ>`: (Optional) An ISO 8601 timestamp for a custom event (e.g., `2024-08-15T18:30:00Z`). The tool will calculate time elapsed or remaining.

### Examples:

1.  **Get sunrise/sunset for Los Angeles today:**
    ```bash
    node src/index.js --lat 34.0522 --lon -118.2437
    ```

2.  **Get sunrise/sunset for London on a specific date:**
    ```bash
    node src/index.js --lat 51.5074 --lon 0.1278 --date 2025-01-01
    ```

3.  **Track time relative to a "Reunion Point" event:**
    ```bash
    node src/index.js --lat 40.7128 --lon -74.0060 --event 2024-08-15T18:30:00Z
    ```

4.  **Combined usage:**
    ```bash
    node src/index.js --lat 34.0522 --lon -118.2437 --date 2024-07-25 --event 2024-07-25T06:00:00Z
    ```

## Development

### Running Tests

```bash
npm test
```
