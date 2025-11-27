# Nightly Log Luminary

## Overview
The Nightly Log Luminary is a simple, self-contained utility designed to bring clarity to your log files. In the post-apocalyptic digital landscape, understanding the whispers and shouts of your systems is crucial. This tool helps you quickly summarize key information from any text-based log file, highlighting errors, warnings, and the most frequently occurring messages.

## Features
- Counts total lines processed.
- Identifies and counts occurrences of 'ERROR', 'WARNING', and 'INFO' messages (case-insensitive).
- Lists the top 5 most frequent unique lines in the log file.

## Usage
```bash
python src/luminary.py <path_to_log_file>
```

### Example
```bash
python src/luminary.py /var/log/syslog
```

## Development
### Requirements
- Python 3.6+

### Running Tests
To run the tests, navigate to the `utils/nightly-log-luminary` directory and execute:
```bash
python -m unittest tests/test_luminary.py
```
