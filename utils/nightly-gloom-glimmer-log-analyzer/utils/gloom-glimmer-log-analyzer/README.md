# Gloom-Glimmer Log Analyzer

## Overview

The `Gloom-Glimmer Log Analyzer` is a whimsical-yet-useful utility designed to provide a quick sentiment analysis of your system logs. It scans log files for predefined 'gloom' (error, warning, critical events) and 'glimmer' (success, info, positive events) keywords, offering a summary of your system's overall 'mood'. Is your system thriving or just barely surviving? This analyzer will tell you!

## How to Use

1.  **Save the script**: Place `analyzer.py` in a directory.
2.  **Run from the command line**: Provide the path to your log file as an argument.

    ```bash
    python3 src/analyzer.py <path_to_your_log_file>
    ```

## Example Output

```
--- Gloom-Glimmer Log Analysis ---
Log File: /var/log/syslog
Total Lines Scanned: 150

Gloom Events:
  - ERROR: 5
  - WARNING: 2
  - CRITICAL: 1
Total Gloom: 8

Glimmer Events:
  - SUCCESS: 25
  - INFO: 100
Total Glimmer: 125

--- Overall System Mood ---
Feeling: Mostly Glimmering! (125 Glimmer vs 8 Gloom)
```
