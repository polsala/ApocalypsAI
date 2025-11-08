# Temporal Anomaly Detector

## Overview

The ApocalypsAI Nightly Integrator presents the 'Temporal Anomaly Detector' – a whimsical yet crucial utility designed to safeguard the integrity of your digital timelines. In the chaotic dance of the apocalypse, even your file system can suffer from temporal distortions. This tool helps you identify files that exist outside their proper chronological sequence, such as those modified in the future or those that have inexplicably aged beyond their years.

Catch misconfigured system clocks, corrupted file systems, or even subtle signs of reality unraveling, all before they lead to catastrophic data inconsistencies.

## Usage

Run the `detector.py` script with the target directory as an argument:

```bash
python src/detector.py --path /path/to/your/directory
```

### Options:

*   `--path <directory>`: The directory to scan (required).
*   `--future-threshold <seconds>`: Report files modified more than this many seconds in the future (default: 0 seconds).
*   `--old-threshold <days>`: Report files modified more than this many days in the past (default: 365 days).

### Example:

```bash
python src/detector.py --path ./my_project --future-threshold 60 --old-threshold 180
```

This will scan `./my_project` for files modified more than 60 seconds in the future, or more than 180 days in the past.

## Output

The script will print a report of any detected anomalies, including the file path, the type of anomaly, and the relevant timestamp. If anomalies are found, the script will exit with a non-zero status code (1); otherwise, it exits with 0.

## Installation

This utility is self-contained and requires Python 3.6+ (or compatible) and standard library modules only. No external dependencies are needed.

```bash
cd utils/temporal-anomaly-detector
python src/detector.py --help
```
