# Chronos-Warp Log Purifier

## Overview

The `chronos-warp-log-purifier` is a utility designed to cleanse your log files of temporal anomalies, redundant entries, and sensitive data patterns. In the chaotic aftermath of an apocalypse (or just a particularly buggy deployment), clean logs are crucial for understanding what went wrong and preparing for the future. This tool helps future historians (and debugging agents) by providing a streamlined, anonymized view of past events.

## Features

*   **Temporal Anomaly Removal**: Strips common timestamp patterns, allowing for easier comparison of log entries regardless of when they occurred.
*   **Redundant Entry Collapsing**: Identical consecutive log lines are collapsed into a single entry, reducing noise and highlighting unique events.
*   **Sensitive Data Redaction**: Automatically identifies and redacts common patterns for API keys, tokens, secrets, and IPv4 addresses, safeguarding sensitive information.

## Usage

To purify a log file, run the `purifier.py` script with the `--input` and `--output` flags:

```bash
python src/purifier.py --input raw_logs.log --output purified_logs.log
```

### Arguments

*   `--input <file_path>`: Path to the raw log file to be purified.
*   `--output <file_path>`: Path where the purified log file will be saved.

## Example

Given a `raw_logs.log` like this:

```
2023-10-27 10:00:01 INFO: Starting system initialization.
2023-10-27 10:00:02 DEBUG: Connecting to database at 192.168.1.100 with API_KEY=sk_live_XXXXXXXXXXXXXXXXXXXX
2023-10-27 10:00:03 INFO: System initialized successfully.
2023-10-27 10:00:03 INFO: System initialized successfully.
2023-10-27 10:00:04 WARNING: Potential anomaly detected. TOKEN=abc123def456
```

The `purified_logs.log` will look like this:

```
INFO: Starting system initialization.
DEBUG: Connecting to database at [REDACTED_IP] with API_KEY=[REDACTED_SECRET]
INFO: System initialized successfully.
WARNING: Potential anomaly detected. TOKEN=[REDACTED_SECRET]
```
