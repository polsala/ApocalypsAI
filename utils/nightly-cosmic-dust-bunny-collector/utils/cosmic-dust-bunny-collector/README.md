# Cosmic Dust Bunny Collector

## Overview
In the post-apocalyptic digital landscape, even the most resilient systems can accumulate 'cosmic dust bunnies' – temporary files, forgotten logs, and empty directories that clutter your precious storage. The Cosmic Dust Bunny Collector is here to help you maintain a pristine and efficient environment.

This Python utility scans specified directories, identifies these digital dust bunnies, and offers to sweep them away, ensuring your system remains lean, mean, and ready for whatever the apocalypse throws at it.

## Features
- Scans for common temporary files (`.tmp`, `.bak`, `.~*`, `#*#`, etc.).
- Identifies truly empty directories.
- Detects old log files (`.log`) based on a configurable age.
- Supports dry-run mode to preview changes before deletion.
- Provides a clear summary of findings and actions.

## Installation
This utility is self-contained. No special installation steps are required beyond having Python 3.8+ installed. Simply navigate to the `src` directory and run the `collector.py` script.

## Usage
```bash
python3 src/collector.py --help
```

### Scan and List (Dry Run)
To see what cosmic dust bunnies are lurking without deleting anything:
```bash
python3 src/collector.py scan /path/to/scan1 /path/to/scan2 --age-days 60
```
(The `scan` command always performs a dry run by default.)

### Clean Up (Actual Deletion)
To actually remove the identified files and directories:
```bash
python3 src/collector.py clean /path/to/scan --age-days 30
```

### Examples
- Scan your home directory for temporary files and empty folders, listing findings:
  ```bash
  python3 src/collector.py scan ~/ --dry-run
  ```
- Clean up log files older than 90 days in `/var/log` (requires appropriate permissions):
  ```bash
  sudo python3 src/collector.py clean /var/log --age-days 90
  ```

## Development & Testing
To run the tests, navigate to the `utils/cosmic-dust-bunny-collector` directory and execute:
```bash
python3 -m unittest tests/test_collector.py
```
