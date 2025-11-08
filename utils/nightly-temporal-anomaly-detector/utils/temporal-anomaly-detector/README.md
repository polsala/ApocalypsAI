# Temporal Anomaly Detector

## Overview

The `temporal-anomaly-detector` is a whimsical-yet-useful Python utility designed to help you spot 'glitches in the matrix' within your log files, data streams, or any text containing timestamps. It's built to identify temporal inconsistencies that might indicate system errors, data corruption, or even subtle shifts in the fabric of reality.

### What it detects:

*   **Out-of-Order Events**: Timestamps that appear before a previous one, suggesting events recorded out of sequence.
*   **Temporal Jumps**: Unusually large gaps or sudden leaps forward/backward in time, potentially indicating clock synchronization issues or data loss.
*   **Impossible Dates**: Dates that don't exist (e.g., February 30th) or are logically impossible within a sequence, pointing to data entry errors or corruption.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No special installation needed. Just run the script directly.
python src/detector.py --help
```

## Usage

Run the `detector.py` script with the path to your log file:

```bash
python src/detector.py --file /path/to/your/log.txt
```

### Options:

*   `--file <path>`: Path to the log file to analyze. (Required)
*   `--threshold <seconds>`: Maximum allowed time difference between consecutive entries before flagging a 'temporal jump'. Default is 3600 seconds (1 hour).
*   `--format <regex>`: Custom regex pattern for timestamp extraction. The pattern must contain a named group `(?P<timestamp>...)`.
*   `--verbose`: Print more detailed information about each anomaly.

### Example:

```bash
python src/detector.py --file my_system_logs.log --threshold 600 --verbose
```

This will scan `my_system_logs.log`, flagging any time jumps greater than 10 minutes, and provide verbose output.

## Detected Anomaly Format

Each detected anomaly will be reported with:

*   **Type**: (e.g., `OUT_OF_ORDER`, `TEMPORAL_JUMP`, `IMPOSSIBLE_DATE`)
*   **Line Number**: The line where the anomaly was detected.
*   **Context**: The full line of text.
*   **Details**: Specific information about the anomaly (e.g., previous timestamp, current timestamp, time difference).

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_detector.py
```
