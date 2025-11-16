# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-vital utility designed to keep your digital cosmos clean and stable. It scans designated log files for 'cosmic dust' – unusual patterns, error spikes, or specific keywords – that might signal an impending system anomaly or 'micro-apocalypse'. By identifying these early warning signs, it helps maintain the integrity of your systems, preventing small issues from escalating into galactic-scale problems.

## Features

*   **Keyword Detection**: Configurable list of keywords (e.g., 'ERROR', 'CRITICAL', 'FAIL') to search for in log files.
*   **Anomaly Spike Detection**: Identifies periods where the density of detected keywords exceeds a defined threshold within a sliding window of log lines.
*   **Configurable Thresholds**: Adjust the sensitivity of anomaly detection.
*   **Multiple Log File Support**: Scan one or many log files in a single run.
*   **Clear Reporting**: Outputs a summary of detected anomalies, including file paths, line numbers, and the nature of the anomaly.

## Usage

```bash
python src/dust_collector.py --log-paths /var/log/syslog /var/log/auth.log --keywords ERROR CRITICAL WARNING --threshold 0.1 --window-size 100
```

### Arguments:

*   `--log-paths` (required): Space-separated list of log file paths to scan.
*   `--keywords` (required): Space-separated list of keywords to search for (case-insensitive).
*   `--threshold` (optional, default: `0.05`): The percentage threshold (0.0 to 1.0) of keyword occurrences within a window to flag as an anomaly. E.g., `0.1` means 10% of lines in a window contain a keyword.
*   `--window-size` (optional, default: `50`): The number of lines in the sliding window for anomaly detection.

## Example Output

```
Starting cosmic dust collection across 2 files...
Scanning log file: /var/log/syslog
  Anomaly detected in /var/log/syslog (lines 10-60): High keyword density (15.00%) detected.
  Anomaly detected in /var/log/syslog (lines 120-170): High keyword density (12.00%) detected.
Scanning log file: /var/log/auth.log
  No significant cosmic dust detected in /var/log/auth.log.

--- Cosmic Dust Report ---
  Anomaly in /var/log/syslog (lines 10-60): High keyword density (15.00%) detected.
  Anomaly in /var/log/syslog (lines 120-170): High keyword density (12.00%) detected.
```

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
cd utils/nightly-cosmic-dust-collector
python src/dust_collector.py --help
```
