# Nightly Chrono-Sync Anomaly Detector

The fabric of spacetime is delicate, and even the slightest temporal drift can have catastrophic consequences for your digital infrastructure. The `nightly-chrono-sync-detector` is your vigilant guardian against such cosmic anomalies, ensuring your system's clock remains perfectly aligned with the universal flow of time.

This whimsical-yet-critical utility leverages `timedatectl` to inspect your system's NTP synchronization status, reporting any temporal misalignments or slumbering chrono-sync services. Keep your servers in harmony with the cosmos!

## Features

*   **Temporal Alignment Check**: Verifies if your system clock is synchronized with NTP.
*   **Anomaly Detection**: Warns if NTP is active but synchronization is lost.
*   **Service Slumber Alert**: Notifies if the NTP service itself is inactive.
*   **Whimsical Output**: Provides status reports with a touch of cosmic flair.

## Usage

To invoke the Chrono-Sync Anomaly Detector, simply run the script:

```bash
./src/chrono_sync_detector.sh
```

The script will output a status message and exit with a code indicating the system's temporal state:
*   `0`: System clock is synchronized (Temporal alignment achieved!).
*   `1`: A temporal anomaly or inactive NTP service is detected (Warning/Error).

### Example Output (Synchronized)

```
STATUS: Temporal alignment achieved! System clock is synchronized with NTP.
```

### Example Output (Unsynchronized)

```
WARNING: Temporal flux detected! NTP service is active, but system clock is NOT synchronized.
```

### Example Output (NTP Service Inactive)

```
WARNING: Chrono-Sync slumbering. NTP service is inactive. System clock may drift.
```

## Requirements

*   A Linux-based system with `systemd` (for `timedatectl`).
*   `bash` (version 4.0 or higher recommended).

## Installation

1.  Navigate to the `bash-utils/nightly-chrono-sync-detector` directory.
2.  Make the script executable:
    ```bash
    chmod +x src/chrono_sync_detector.sh
    ```
3.  Run it as shown in the Usage section.

## Testing

To run the automated tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_chrono_sync_detector.sh
```

The tests use a mocked `timedatectl` command to simulate various NTP synchronization states, ensuring deterministic and offline verification of the detector's logic.
