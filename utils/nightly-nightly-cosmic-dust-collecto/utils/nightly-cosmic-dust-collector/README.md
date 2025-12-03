# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you keep an eye on the health of your systems and agent runs. It scans through log files, sifting through the 'cosmic dust' to find 'anomalies' – specific error patterns that might indicate a problem.

Think of it as your personal log-file astrologer, pointing out the constellations of trouble before they become supernovas.

## Features

*   **Pattern-based Scanning**: Define custom patterns (e.g., 'ERROR', 'FAIL', 'Exception') to search for in your log files.
*   **Recursive Directory Scan**: Scans all `.log` files within a specified directory and its subdirectories.
*   **Anomaly Summary**: Provides a summary of total anomalies found, unique anomaly lines, and counts per pattern.
*   **Self-contained**: Written in Python, with minimal dependencies, making it easy to run anywhere.

## Usage

```bash
python src/collector.py --path <directory_to_scan> [--patterns <pattern1> <pattern2> ...]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning for log files.
*   `--patterns <pattern1> <pattern2> ...`: (Optional) One or more patterns to search for. If not provided, defaults to `['ERROR', 'FAIL', 'Exception', 'Traceback']`.

### Example:

To scan the `logs/` directory for default error patterns:

```bash
python src/collector.py --path logs/
```

To scan the `agent_runs/` directory for specific patterns 'CRITICAL' and 'Timeout':

```bash
python src/collector.py --path agent_runs/ --patterns CRITICAL Timeout
```

## Installation

This utility is self-contained. Simply place the `nightly-cosmic-dust-collector` folder in your `utils/` directory. No special installation steps are required beyond having Python 3.11+ installed.

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_collector.py
```
