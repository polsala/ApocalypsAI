# Nightly Chronos Drift Detector

## Overview

The `nightly-chronos-drift-detector` is a whimsical yet crucial utility designed to scan your file system for 'temporal anomalies'. In simpler terms, it looks for files whose modification or creation timestamps are suspiciously in the future, or significantly out of sync with the current system time. This can be an early warning sign of system clock issues, corrupted file metadata, or even subtle forms of data corruption.

Think of it as a digital time-traveler's compass, pointing out where your files might be experiencing a 'chronos drift'.

## Usage

```bash
python src/detector.py --path /path/to/scan1 --path /path/to/scan2 --future-threshold 300 --past-threshold 86400
```

### Arguments:

*   `--path <directory>`: One or more directories to scan. (Required, can be specified multiple times)
*   `--future-threshold <seconds>`: Files modified/created more than this many seconds in the future will be flagged. Default: `60` (1 minute).
*   `--past-threshold <seconds>`: Files modified/created more than this many seconds in the past (relative to the current time) will be flagged. This is useful for identifying unusually old or stale files. Default: `0` (disabled).
*   `--report-all`: If set, reports all files found, not just those with drift. Useful for debugging or full audits. Default: `False`.

## Examples

Scan your home directory for future-dated files, allowing up to 5 minutes of future drift (e.g., for network sync delays):

```bash
python src/detector.py --path ~/ --future-threshold 300
```

Scan a project directory for any file dated more than 24 hours in the past (useful for finding ancient build artifacts):

```bash
python src/detector.py --path /my/project --past-threshold 86400
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

```bash
cd utils/nightly-chronos-drift-detector
python src/detector.py --help
```
