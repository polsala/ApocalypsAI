# Nightly Gloom-Glimmer Log Analyzer

## Overview

The 'Nightly Gloom-Glimmer Log Analyzer' is a whimsical utility designed to help you quickly gauge the 'mood' of your system's log files. Instead of just listing errors, it assigns a 'Gloom-Glimmer Score' based on the presence of predefined 'gloom' (errors, warnings) and 'glimmer' (successes, important events) patterns. It then provides a lighthearted, apocalypse-themed summary of your logs' overall sentiment.

This tool is perfect for those moments when you need a quick sanity check on your systems, but also a chuckle to keep the existential dread at bay.

## Usage

To analyze a log file, run the `analyzer.py` script with the path to your log file:

```bash
python src/analyzer.py <path_to_your_log_file>
```

### Example Output:

```
Analyzing log file: /var/log/syslog

--- Gloom-Glimmer Report ---

Total Lines Scanned: 150
Gloom Events (Errors, Warnings, etc.): 12
Glimmer Events (Successes, Info, etc.): 35

Gloom-Glimmer Score: +23

Overall Sentiment: A faint glimmer of hope pierces the perpetual twilight. Your systems are mostly holding together, but keep an eye on those flickering lights.

----------------------------
```

## Configuration

The `analyzer.py` script contains default patterns for 'gloom' and 'glimmer' events. You can modify these regular expressions directly within the `analyzer.py` file to suit your specific log formats and desired keywords.

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

To run tests:

```bash
python -m unittest tests/test_analyzer.py
```
