# Temporal Drift Detector

## Chronological Integrity in a Chaotic Universe

This utility, the "Temporal Drift Detector," is designed to monitor your system's clock for unusual jumps, skips, or drifts. In an era where even time itself might be a conspiracy, ensuring chronological integrity is paramount. Whether you're debugging time-sensitive distributed systems, verifying NTP synchronization, or simply preparing for a temporal anomaly, this tool provides a whimsical yet critical check.

It's a simple Python script that records the last known "good" timestamp and, upon subsequent runs, compares the current system time against the expected progression. If the time difference deviates significantly from the expected interval, it flags a potential temporal anomaly.

## Usage

### Prerequisites

*   Python 3.11+

### Running the Detector

1.  Navigate to the `utils/temporal-drift-detector` directory.
2.  Run the script:
    ```bash
    python src/detector.py
    ```

The script will:
*   Read the last recorded timestamp from `.last_time` (or initialize it if not found).
*   Compare the current time with the last recorded time, considering an expected interval (default: 60 seconds, configurable) and a drift tolerance (default: 5 seconds, configurable).
*   Report any detected anomalies.
*   Update `.last_time` with the current timestamp.

### Configuration

You can adjust the expected interval and drift tolerance by modifying the `EXPECTED_INTERVAL_SECONDS` and `DRIFT_TOLERANCE_SECONDS` constants in `src/detector.py`.

### Example Output

```
[INFO] No previous timestamp found. Initializing .last_time.
[INFO] Current time recorded: 1678886400.0

[INFO] Last recorded time: 1678886400.0, Current time: 1678886460.5
[INFO] Expected interval: 60.0s, Actual elapsed: 60.5s, Drift: 0.5s
[INFO] Time is within expected bounds.

[WARNING] Last recorded time: 1678886460.5, Current time: 1678886580.0
[WARNING] Expected interval: 60.0s, Actual elapsed: 119.5s, Drift: 59.5s
[ERROR] Temporal anomaly detected! Time jumped by 59.5 seconds beyond tolerance.
```
