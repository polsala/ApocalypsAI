# Nightly Chrono-Compass Calibrator

The fabric of spacetime is delicate, and even the slightest temporal distortion can lead to unforeseen anomalies in your system's logs, security protocols, and distributed operations. The **Nightly Chrono-Compass Calibrator** is a whimsical-yet-critical utility designed to ensure your system's internal clock remains perfectly synchronized with the cosmic rhythm of Network Time Protocol (NTP).

This utility scans for common NTP clients (like `timedatectl`, `chronyc`, or `ntpdate`), queries their status, and reports any detected temporal drift. It then assigns a "Temporal Stability Score" to give you a quick overview of your system's temporal alignment.

## Features

*   **Multi-Client Support**: Automatically detects and uses `timedatectl` (for `systemd-timesyncd`), `chronyc` (for `chronyd`), or `ntpdate` to check NTP synchronization.
*   **Drift Detection**: Quantifies the system's time offset from NTP servers.
*   **Temporal Status Reporting**: Categorizes drift into "STABLE", "MINOR_DRIFT", or "MAJOR_DRIFT".
*   **Whimsical Stability Score**: Provides a "Temporal Stability Score" out of 100, reflecting the precision of your system's time.
*   **Actionable Warnings**: Alerts you to significant temporal distortions that require attention.

## Usage

### Prerequisites

You need at least one of the following NTP clients installed and configured on your system:
*   `systemd-timesyncd` (managed via `timedatectl`)
*   `chronyd` (managed via `chronyc`)
*   `ntpdate` (legacy NTP client)

### Running the Calibrator

Navigate to the `src` directory and execute the script:

```bash
./chrono_compass.sh
```

The script will output a report similar to this:

```
Nightly Chrono-Compass Calibrator Initiating Temporal Scan...
---------------------------------------------------
Using timedatectl for temporal readings.
Detected temporal offset: 0 ms
Temporal Status: STABLE
Temporal Stability Score: 100/100
The Chrono-Compass hums contentedly. Temporal alignment is pristine!
```

Or, if drift is detected:

```
Nightly Chrono-Compass Calibrator Initiating Temporal Scan...
---------------------------------------------------
Using chronyc for temporal readings.
Detected temporal offset: 120 ms
Temporal Status: MINOR_DRIFT
Temporal Stability Score: 88/100
A slight shimmer in the temporal fabric. Minor adjustments may be needed.
```

In case of major drift:

```
Nightly Chrono-Compass Calibrator Initiating Temporal Scan...
---------------------------------------------------
Using ntpdate for temporal readings.
Detected temporal offset: 550 ms
Temporal Status: MAJOR_DRIFT
Temporal Stability Score: 45/100
WARNING: The Chrono-Compass is wildly spinning! Significant temporal distortion detected!
Immediate recalibration recommended to prevent timeline anomalies.
```

### Exit Codes

*   `0`: Temporal alignment is STABLE or MINOR_DRIFT.
*   `1`: MAJOR_DRIFT detected or no suitable NTP client found.

## Development & Testing

### Running Tests

To run the automated tests, navigate to the `tests` directory and execute the test script:

```bash
./test_chrono_compass.sh
```

The tests use mock functions to simulate the output of `timedatectl`, `chronyc`, and `ntpdate` without requiring actual system changes or network access, ensuring deterministic and offline validation.
