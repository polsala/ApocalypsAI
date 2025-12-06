# Cataclysmic Event Log Analyzer

## Overview

The `cataclysmic-event-log-analyzer` is a whimsical yet genuinely useful utility designed to help ApocalypsAI agents quickly identify potential system failures, anomalies, or 'precursor events' to a full-blown apocalypse by scanning log files for critical messages.

It parses log files, looking for keywords like `ERROR`, `CRITICAL`, `WARNING`, `FAILURE`, `FATAL`, `APOCALYPSE`, and `DOOM`, and provides a summarized report of all detected 'cataclysmic' events.

## Features

*   **Keyword-based Detection**: Identifies critical events using a predefined list of severity keywords.
*   **Multi-file Support**: Can process one or more log files.
*   **Summarized Report**: Outputs a clear, chronological list of detected events with their line numbers and messages.
*   **Self-contained**: Written in Python, with no external dependencies beyond standard library.

## Installation

This utility is self-contained. Simply ensure you have Python 3.6+ installed.

## Usage

Run the `analyzer.py` script from the `src/` directory, providing one or more log file paths as arguments:

```bash
python3 src/analyzer.py path/to/log1.log path/to/another/log.txt
```

### Example Output

```
--- Cataclysmic Event Report ---

Detected 3 potential cataclysmic events:

[log1.log:L5] WARNING: Disk space low on /dev/sda1
[log1.log:L12] ERROR: Database connection failed
[another/log.txt:L23] CRITICAL: Core system meltdown imminent!

--- End Report ---
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
python3 -m unittest tests/test_analyzer.py
```
