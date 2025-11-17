# Nightly Log Whisperer

The digital wasteland is vast, and its echoes are often found in the endless streams of log files. The Nightly Log Whisperer is your essential tool for sifting through the noise, identifying critical messages, and generating concise reports to keep your systems operational amidst the chaos.

## Purpose

This utility scans specified log files for predefined keywords (e.g., `ERROR`, `WARNING`, `CRITICAL`) and compiles a summary report, highlighting the occurrences and their context. It's designed to help you quickly pinpoint issues without drowning in verbose logs.

## Usage

```bash
python src/log_whisperer.py --log-file /path/to/your/log.log --keywords ERROR WARNING --output-file report.txt
```

### Arguments

*   `--log-file <path>`: Path to the log file to be analyzed. (Required)
*   `--keywords <keyword1> [<keyword2> ...]`: Space-separated list of keywords to search for. Case-insensitive. (Default: `ERROR WARNING CRITICAL`)
*   `--output-file <path>`: Path to save the summary report. If not provided, the report will be printed to stdout.
*   `--context-lines <int>`: Number of lines before and after a keyword match to include in the report for context. (Default: `2`)

## Example Report

```
--- Log Whisperer Report ---
Scan Date: 2023-10-27 04:42:00

Log File: /var/log/syslog

Keywords Searched: ERROR, WARNING, CRITICAL

--- Summary ---
Total lines scanned: 1500
Matches found: 5

--- Details ---

[Match 1] Keyword: ERROR (Line 123)
Context:
  Line 121: [INFO] Processing request for user_id=123
  Line 122: [DEBUG] Database connection pool status: OK
  Line 123: [ERROR] Failed to connect to external service: Connection refused
  Line 124: [INFO] Retrying connection in 5 seconds...
  Line 125: [DEBUG] Current retry attempt: 1

[Match 2] Keyword: WARNING (Line 456)
Context:
  Line 454: [INFO] Disk usage check initiated.
  Line 455: [DEBUG] /dev/sda1 usage: 85%
  Line 456: [WARNING] Disk usage on /dev/sda1 is approaching critical levels (85%)
  Line 457: [INFO] Initiating cleanup process...
  Line 458: [DEBUG] Cleanup process completed.

--- End Report ---
```
