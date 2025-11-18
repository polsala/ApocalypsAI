# Nightly Temporal Anomaly Tracker

## Purpose
In the chaotic aftermath, even the digital clockwork can go awry. The `Nightly Temporal Anomaly Tracker` is your personal chronometer for the file system, designed to detect files with modification timestamps that are suspiciously in the future, or excessively old. This can help uncover system clock synchronization issues, forgotten digital artifacts, or even evidence of rogue time-traveling processes.

## Usage

Run the `tracker.py` script with the target directory and optional thresholds:

```bash
python src/tracker.py --path /path/to/scan --future-threshold-days 1 --old-threshold-days 365
```

### Arguments:
*   `--path <directory>`: The directory to scan for temporal anomalies. (Required)
*   `--future-threshold-days <int>`: Files modified more than this many days in the future are flagged. Default: 0 (any future modification).
*   `--old-threshold-days <int>`: Files not modified for more than this many days are flagged as 'ancient'. Default: 365.

## Output
The script will print a list of files identified as having temporal anomalies, categorized by type (Future or Ancient). If any anomalies are found, the script will exit with code `1`; otherwise, it exits with `0`.

## Example

```
Scanning /home/user/data for temporal anomalies...

--- Temporal Anomalies Detected ---

Future Modifications (modified > 0 days in the future):
  - /home/user/data/future_log.txt (Modified: 2025-01-01 12:00:00 UTC, Current: 2024-01-01 12:00:00 UTC)

Ancient Artifacts (not modified for > 365 days):
  - /home/user/data/old_report.pdf (Modified: 2020-05-10 08:00:00 UTC, Current: 2024-01-01 12:00:00 UTC)

Scan complete.
```
