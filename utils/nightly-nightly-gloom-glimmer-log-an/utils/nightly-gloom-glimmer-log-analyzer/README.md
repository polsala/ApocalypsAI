# Nightly Gloom-Glimmer Log Analyzer

## Overview

In the post-apocalyptic digital wasteland, even system logs can be a source of despair... or a beacon of hope! The Nightly Gloom-Glimmer Log Analyzer is a whimsical-yet-useful utility designed to sift through your system logs, identifying patterns of "gloom" (errors, warnings, failures) and "glimmer" (successes, recoveries, positive status updates). It provides a concise summary, helping you gauge the overall morale and operational status of your vital systems.

Keep your spirits up by focusing on the glimmers, while staying vigilant against the gloom!

## Usage

The analyzer is a Python script that takes a log file path as an argument.

```bash
python src/analyzer.py <path_to_log_file>
```

### Example

Given a `system.log` file:

```
2023-10-27 08:00:01 INFO System startup initiated.
2023-10-27 08:00:05 ERROR Failed to connect to external sensor array. Retrying...
2023-10-27 08:00:10 SUCCESS Data backup completed.
2023-10-27 08:00:15 WARNING Low power detected on auxiliary unit.
2023-10-27 08:00:20 INFO Resource allocation optimized.
2023-10-27 08:00:25 RECOVERY External sensor array reconnected.
2023-10-27 08:00:30 CRITICAL Core meltdown imminent. Just kidding! System stable.
```

Running `python src/analyzer.py system.log` would produce:

```
--- Gloom-Glimmer Log Analysis ---
Log File: system.log

Gloom (Negative Events):
  - ERROR: 2 occurrence(s)
  - WARNING: 1 occurrence(s)
Total Gloom Events: 3

Glimmer (Positive Events):
  - SUCCESS: 3 occurrence(s)
  - INFO: 1 occurrence(s)
Total Glimmer Events: 4

Overall Morale: Optimistic! Glimmers outshine the Gloom.
```

## Development

The utility is written in Python 3.11 and is self-contained.
Tests are located in `tests/test_analyzer.py` and can be run using `pytest` or `python -m unittest`.
