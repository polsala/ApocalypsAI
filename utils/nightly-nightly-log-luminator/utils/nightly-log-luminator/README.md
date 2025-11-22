# Nightly Log Luminator

## Overview

The Nightly Log Luminator is a whimsical-yet-useful utility designed to bring clarity to the chaotic digital logs of your systems. In the post-apocalyptic landscape of data, understanding what went wrong (or what's just... weird) is crucial for survival. This tool scans specified log files, identifies common error patterns, summarizes their occurrences, and highlights lines that don't fit any known patterns, pointing out potential anomalies.

## Features

*   **Pattern-based Error Detection**: Configurable regex patterns to catch common issues like 'ERROR', 'WARNING', 'EXCEPTION', 'CRITICAL', 'FAILED', 'DENIED'.
*   **Anomaly Highlighting**: Identifies log lines that don't match any defined patterns, potentially indicating new or unusual events.
*   **Summary Report**: Provides a concise overview of detected errors and anomalies.
*   **Self-contained**: Written in Python, with no external dependencies beyond the standard library.

## Usage

To use the Log Luminator, simply run the `luminator.py` script with the path to your log file:

```bash
python3 src/luminator.py /path/to/your/logfile.log
```

### Example Output

```
--- Log Luminator Report ---

Scanning: /path/to/your/logfile.log

Detected Patterns:
  CRITICAL: 1 occurrence
  ERROR: 2 occurrences
  WARNING: 1 occurrence

Anomalous Lines (3 total):
  - INFO: App started
  - DEBUG: Heartbeat
  - Unknown anomaly detected.

--- End Report ---
```

## Configuration

The default error patterns are defined within `src/luminator.py` in the `get_default_patterns` function. You can modify these regex patterns to suit your specific logging needs.

## Development

To run tests:

```bash
python3 -m unittest tests/test_luminator.py
```
