# Temporal Anomaly Detector

## Whimsical Purpose

In the grand scheme of ApocalypsAI, even data can suffer from temporal distortions! The Temporal Anomaly Detector is your first line of defense against files that are suspiciously ancient or alarmingly fresh. Is that critical configuration file from 2005, or did someone just create a new "backup" that's only 3 seconds old? This utility helps you spot these temporal oddities before they unravel the fabric of your digital reality.

## Practical Use

This utility scans a specified directory for files whose modification timestamps fall outside a defined "normal" range. It flags:
- **"Too Old" files**: Potentially stale caches, forgotten backups, or data that hasn't been updated in an unacceptably long time.
- **"Too New" files**: Unexpected creations, rapid changes, or files that might indicate recent, unauthorized activity or a system clock issue.

It's useful for:
- **Data Integrity Checks**: Ensure critical files are being updated as expected.
- **Security Monitoring**: Detect new, unexpected files or old, forgotten ones that could be vulnerabilities.
- **System Health**: Identify processes creating too many temporary files or failing to clean up old ones.

## Usage

The detector is a Python 3.11 script.

```bash
python src/detector.py <directory_to_scan> [--max-age-days <days>] [--min-age-seconds <seconds>]
```

### Arguments

- `<directory_to_scan>`: **Required**. The path to the directory you want to scan for anomalies.
- `--max-age-days <days>`: Optional. Files older than this many days will be flagged as "too old". Default is `30` days.
- `--min-age-seconds <seconds>`: Optional. Files newer than this many seconds will be flagged as "too new". Default is `5` seconds.

### Example

Scan the `/var/log` directory, flagging files older than 7 days or newer than 60 seconds:

```bash
python src/detector.py /var/log --max-age-days 7 --min-age-seconds 60
```

### Exit Codes

- `0`: No temporal anomalies detected.
- `1`: One or more temporal anomalies detected.

## Example Output (Anomalies Detected)

```
Scanning '/path/to/my/data' for temporal anomalies...
  Max age for 'too old': 30 days
  Min age for 'too new': 5 seconds

--- Temporal Anomalies Detected! ---

Files that are suspiciously old:
- /path/to/my/data/archive/legacy_report.csv (Modified: 2022-01-15T10:30:00)
- /path/to/my/data/config/old_settings.conf (Modified: 2023-08-01T14:00:00)

Files that are surprisingly new:
- /path/to/my/data/temp/new_temp_file.tmp (Modified: 2023-10-26T11:59:58)
```

## Example Output (No Anomalies)

```
Scanning '/path/to/my/data' for temporal anomalies...
  Max age for 'too old': 30 days
  Min age for 'too new': 5 seconds

No temporal anomalies detected. All clear!
```
