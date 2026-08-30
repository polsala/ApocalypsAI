# Nightly Chrono-Compass Calibrator

## Unveiling Temporal Drift and Harmonizing Your Chrono-Compass

In the ever-shifting currents of the post-apocalyptic timeline, maintaining a perfectly synchronized Chrono-Compass is paramount. The **Nightly Chrono-Compass Calibrator** is a whimsical yet vital utility designed to detect "Temporal Drift Anomalies" in your system's clock and guide you towards temporal harmony.

It fetches the true, unyielding time from the "Temporal Beacon Network" (our reliable external time source) and compares it against your local system's Chrono-Compass. Any discrepancy is reported as a "Temporal Drift Anomaly," allowing you to take corrective action.

## Features

*   **Temporal Drift Detection**: Accurately measures the difference between your system's time and a global temporal beacon.
*   **Whimsical Reporting**: Presents drift information with a touch of post-apocalyptic charm.
*   **Cross-Platform**: Built with Node.js, it works wherever Node.js runs.
*   **Actionable Advice**: Provides guidance on how to re-synchronize your system's Chrono-Compass.

## Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-chrono-calibrator
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

To check your temporal alignment:

```bash
node src/index.js
```

### Options

*   `--no-color`: Disable colored output.

### Example Output

```
🌌 Initiating Chrono-Compass Calibration...
📡 Contacting Temporal Beacon Network...
✅ Temporal Beacon Network responded with true time: 1701388800 (Unix Epoch)
⏳ Your local Chrono-Compass reads: 1701388805 (Unix Epoch)

⚠️ Temporal Drift Anomaly Detected!
Your Chrono-Compass is drifting by +5.000 seconds (ahead of true time).

To re-harmonize your Chrono-Compass, consider these actions:
- On Linux/macOS: `sudo ntpdate -u pool.ntp.org` or `sudo systemctl restart systemd-timesyncd`
- On Windows: Open 'Date & Time settings' and click 'Sync now' or run `w32tm /resync` in an elevated command prompt.
```

## Development & Testing

To run the automated tests:

```bash
npm test
```
