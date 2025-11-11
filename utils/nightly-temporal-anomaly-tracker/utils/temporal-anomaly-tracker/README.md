# Temporal Anomaly Tracker

## Overview

The `temporal-anomaly-tracker` is a whimsical-yet-useful utility designed to monitor your system's clock for significant deviations, which it playfully labels as 'temporal anomalies.' In the grand scheme of the ApocalypsAI, maintaining precise time synchronization is crucial, whether for coordinating agent actions, timestamping critical events, or simply ensuring your doomsday device's countdown is accurate.

This tool compares your local system time against a simulated external reference (which, in a real-world scenario, would be a reliable Network Time Protocol (NTP) server) and alerts you if the drift exceeds a configurable threshold. While its output is flavored with apocalyptic whimsy, its core function is a serious check for clock drift, which can lead to subtle but critical issues in distributed systems, logging, security, and data consistency.

## How it Works

1.  **Local Time Capture**: It fetches the current time from your system.
2.  **Reference Time Simulation**: It obtains a 'reference' time. For offline testing, this is a controlled mock. In a production environment, this would typically involve querying a reliable external time source.
3.  **Drift Calculation**: The difference between your local time and the reference time is calculated.
4.  **Anomaly Detection**: If the absolute drift exceeds a predefined threshold (defaulting to 5 seconds), a 'Temporal Anomaly' is reported, and the utility exits with a non-zero status code.

## Usage

To run the tracker, navigate to the `utils/temporal-anomaly-tracker` directory and execute the `tracker.py` script:

```bash
python3 src/tracker.py
```

### Example Output (No Anomaly):

```text
Initiating Temporal Anomaly Scan...
Local Time: 2023-10-27T10:00:00.123456
Reference Time: 2023-10-27T10:00:00.000000 (simulated external source)
Time Drift: 0.12 seconds
✅ All temporal vectors aligned. No anomalies detected.
```

### Example Output (Anomaly Detected):

```text
Initiating Temporal Anomaly Scan...
Local Time: 2023-10-27T10:00:15.789012
Reference Time: 2023-10-27T10:00:00.000000 (simulated external source)
Time Drift: 15.79 seconds
🚨 TEMPORAL ANOMALY DETECTED! Drift of 15.79 seconds exceeds threshold.
```

## Development & Testing

The utility is written in Python 3.11 and is self-contained. Tests are provided to ensure the anomaly detection logic works as expected under various drift scenarios, using mocks to simulate different time states.

To run tests:

```bash
python3 -m unittest utils/temporal-anomaly-tracker/tests/test_tracker.py
```

## Configuration

The `threshold_seconds` for anomaly detection can be adjusted within the `detect_anomaly` function in `src/tracker.py` if a different sensitivity is required for your temporal monitoring needs.
