# Nightly Log Whisperer

## Overview
In the quiet aftermath, even your logs can hold secrets of impending digital doom. The `Nightly Log Whisperer` is a whimsical yet crucial utility designed to listen to the whispers of your system logs. It scans specified directories for recent log files, identifies common error patterns, and provides a concise summary of potential issues, helping you maintain a vigilant watch over your digital outposts.

## Features
- Scans log files (`.log`, `.txt`) within a specified directory and time window.
- Detects common error keywords (e.g., `ERROR`, `FAIL`, `EXCEPTION`, `CRITICAL`, `FATAL`).
- Summarizes total errors, files scanned, and the most frequent error messages.
- Lightweight and self-contained, perfect for nightly system health checks.

## Usage

```bash
python src/whisperer.py --path /var/log --hours 24
```

### Arguments:
- `--path <directory>`: The directory to scan for log files (e.g., `/var/log`, `./logs`).
- `--hours <int>`: The time window in hours to consider log files (e.g., `24` for the last 24 hours). Defaults to `24`.

## Example Output

```
Nightly Log Whisperer Report
----------------------------

Scanning directory: /var/log
Time window: 24 hours

Files scanned: 5
Total error lines found: 12

Top 5 Error Messages:
1. [ERROR] Failed to connect to database (5 occurrences)
2. [CRITICAL] Disk space low (3 occurrences)
3. [EXCEPTION] NullPointerException (2 occurrences)
4. [ERROR] Timeout waiting for response (1 occurrence)
5. [FATAL] Unhandled system error (1 occurrence)

All clear, for now. Keep whispering!
```
