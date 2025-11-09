# Temporal Anomaly Detector

## Purpose
This utility, the 'Temporal Anomaly Detector', is designed to monitor your system's clock for any unusual behavior, such as sudden jumps forward or backward in time, or a consistent drift (running too fast or too slow). While whimsically named to detect 'temporal anomalies', its practical use is to identify critical system clock issues that can impact logging, security, and distributed system synchronization.

## Features
- **Jump Detection**: Identifies sudden, large changes in the system clock (e.g., if the clock is manually reset or synchronized).
- **Drift Detection**: Monitors for sustained discrepancies between the system clock and actual elapsed time.
- **Configurable Thresholds**: Allows customization of what constitutes an 'anomaly'.

## Usage
To run the detector, simply execute the Python script. It will continuously monitor the system time.

```bash
python3 src/detector.py
```

### Configuration
You can adjust the following parameters within `src/detector.py`:
- `CHECK_INTERVAL_SECONDS`: How often the clock is checked.
- `TIME_JUMP_THRESHOLD_SECONDS`: The minimum number of seconds for a time jump to be considered an anomaly.
- `DRIFT_THRESHOLD_PERCENT`: The maximum allowed percentage difference between system time elapsed and real time elapsed over an interval.

## Example Output
```
[2023-10-27 10:00:00] [TemporalAnomalyDetector] Initialized monitoring.
[2023-10-27 10:00:10] [TemporalAnomalyDetector] ANOMALY DETECTED: Time jumped forward by 3600.0 seconds!
[2023-10-27 11:00:20] [TemporalAnomalyDetector] ANOMALY DETECTED: System clock drifted fast by +15.0% (expected 10.0s, got 11.5s)
[2023-10-27 11:00:30] [TemporalAnomalyDetector] Detector stopped by user.
```

## Installation
No special installation required. Ensure you have Python 3.6+ installed.
