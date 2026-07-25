# Nightly Chrono-Compass Calibrator

A Node.js CLI utility designed to help survivors synchronize their system clocks with the elusive "Temporal Anchor" – a mythical post-apocalyptic NTP server. For those who crave a touch of the unpredictable, it can also introduce minor, whimsical temporal distortions, ensuring your time isn't just accurate, but *interestingly* accurate.

## Features

*   **System Time Synchronization**: Compares your local system time with a simulated "Temporal Anchor" server.
*   **Suggested Correction**: Provides a `date` command (for Linux/macOS) to correct your system time.
*   **Whimsical Distortion**: Optionally introduces a small, random time shift (e.g., ±5 seconds) to keep things lively.
*   **Cross-Platform**: Designed as a Node.js CLI, making it runnable on various operating systems.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Navigate to the utility's directory:
    ```bash
    cd node-utils/nightly-chrono-compass-calibrator
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the calibrator from the utility's directory:

```bash
node src/index.js [options]
```

### Options

*   `-s, --server <url>`: (Optional) Specify the URL of the "Temporal Anchor" NTP server. Defaults to `https://apocalypsai.time.anchor`. (Note: This is a simulated server for whimsical purposes).
*   `-d, --distort`: (Optional) Enable whimsical temporal distortion. Adds a small, random offset to the calculated time.
*   `-h, --help`: Display help for command.

### Examples

**1. Calibrate without distortion:**

```bash
node src/index.js
```

*Expected Output:*
```
[Chrono-Compass] Calibrating with Temporal Anchor: https://apocalypsai.time.anchor
[Chrono-Compass] Local Time: 2023-10-27T10:00:00.000Z
[Chrono-Compass] Anchor Time: 2023-10-27T10:00:05.123Z
[Chrono-Compass] Time difference: +5.123 seconds.
[Chrono-Compass] Suggested command to synchronize:
    sudo date -s "2023-10-27 10:00:05"
```

**2. Calibrate with distortion:**

```bash
node src/index.js --distort
```

*Expected Output:*
```
[Chrono-Compass] Calibrating with Temporal Anchor: https://apocalypsai.time.anchor
[Chrono-Compass] Local Time: 2023-10-27T10:00:00.000Z
[Chrono-Compass] Anchor Time: 2023-10-27T10:00:05.123Z
[Chrono-Compass] Applying whimsical temporal distortion... (+2.345 seconds)
[Chrono-Compass] Effective Anchor Time: 2023-10-27T10:00:07.468Z
[Chrono-Compass] Time difference: +7.468 seconds.
[Chrono-Compass] Suggested command to synchronize:
    sudo date -s "2023-10-27 10:00:07"
```

## Development

### Running Tests

```bash
npm test
```

### Project Structure

```
.
├── README.md
├── package.json
├── src/
│   └── index.js            # Main CLI application
└── tests/
    └── index.test.js       # Jest tests
```
