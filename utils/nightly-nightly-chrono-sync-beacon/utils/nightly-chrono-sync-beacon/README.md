# Nightly Chrono-Sync Beacon

## Overview

The Nightly Chrono-Sync Beacon is a whimsical yet crucial utility designed to help you maintain temporal integrity across your systems. In a world where digital timelines can easily drift, this beacon ensures your system clock is perfectly aligned with a trusted reference, reporting any discrepancies.

Think of it as your personal time-lord, making sure your servers aren't running on 'wibbly-wobbly, timey-wimey' schedules.

## Features

*   **Drift Detection**: Compares your system's current time against a configurable reference time source.
*   **Threshold Alerting**: Reports drift only if it exceeds a specified threshold, preventing unnecessary alarms.
*   **Simple & Self-Contained**: Easy to integrate and run, with minimal dependencies.

## Usage

```bash
python src/chrono_sync.py --threshold 5
```

This will check your system's time against a default reference (e.g., a hardcoded mock for demonstration, or an NTP server in a more advanced setup) and report if the drift is greater than 5 seconds.

### Arguments

*   `--threshold <seconds>`: The maximum acceptable time drift in seconds. Defaults to 1 second.

## Development Notes

For testing purposes, the reference time source is mocked to ensure deterministic and offline tests. In a production environment, this would typically be replaced with a call to an NTP server or a similar reliable time source.
