# Nightly Gloom-Glimmer Log Scrubber

## Overview
In the digital wasteland, log files can be vast and overwhelming, filled with noise and irrelevant data. The Gloom-Glimmer Log Scrubber is your trusty companion, designed to cut through the digital 'gloom' and highlight the 'glimmers' of critical information. It helps you quickly identify important events, errors, or anomalies by filtering out common noise and emphasizing specified keywords.

## Features
- **Configurable Filtering**: Define keywords to ignore (e.g., common debug messages) and keywords to highlight (e.g., 'ERROR', 'CRITICAL', 'ALERT').
- **Case-Insensitive Matching**: Keywords and log lines are compared without regard to case.
- **Simple CLI Interface**: Easily specify your log file and configuration file.
- **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation
This utility is self-contained. Simply place the `nightly-gloom-glimmer-log-scrubber` folder in your desired location.

## Usage

```bash
python src/scrubber.py --log-file <path_to_log_file> --config-file <path_to_config_file>
```

### Configuration File Example (`config.json`)

Create a JSON file (e.g., `config.json`) to define your filtering rules:

```json
{
  "keywords_to_highlight": [
    "ERROR",
    "CRITICAL",
    "FAILURE",
    "ALERT"
  ],
  "keywords_to_ignore": [
    "DEBUG",
    "INFO",
    "heartbeat",
    "connection established"
  ]
}
```

### Example Run

Given a `sample.log`:
```
INFO: User 'admin' logged in.
DEBUG: Processing request for /api/status.
Error: Database connection failed.
INFO: Task 'backup' completed successfully.
CRITICAL: System overload detected!
DEBUG: heartbeat signal received.
```

And `config.json` as above, running the scrubber will output:

```
Error: Database connection failed.
CRITICAL: System overload detected!
```

## Development

### Running Tests

```bash
python -m unittest tests/test_scrubber.py
```
