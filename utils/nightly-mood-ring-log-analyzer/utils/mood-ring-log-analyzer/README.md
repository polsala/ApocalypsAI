# Mood-Ring Log Analyzer

## Overview

The `mood-ring-log-analyzer` is a whimsical utility designed to give you a quick, intuitive glance at the 'emotional state' of your system's log files. Instead of sifting through endless lines, this tool processes your logs and assigns an overall 'mood' – from 'Serene' to 'Critical' – based on the prevalence of different log levels.

It's perfect for a rapid health check, helping you spot potential issues before they escalate, all while adding a touch of playful insight to your daily operations.

## Features

*   **Mood-Based Analysis**: Categorizes log entries into 'Calm', 'Anxious', 'Critical', and 'Mysterious' moods.
*   **Overall System Mood**: Determines the dominant mood of the entire log file based on a priority system (Critical > Anxious > Calm > Mysterious).
*   **Summary Report**: Provides a count of each mood category and a final system mood with a descriptive message.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.

## Usage

To analyze a log file, simply run the script with the path to your log file:

```bash
python src/analyzer.py <path_to_your_log_file>
```

### Example Output:

```
Analyzing log file: /var/log/syslog

--- Mood-Ring Log Analysis ---

Mood Counts:
  Calm: 125 (INFO, DEBUG, NOTICE)
  Anxious: 12 (WARNING, WARN)
  Critical: 3 (ERROR, CRITICAL, FATAL)
  Mysterious: 5 (Unrecognized entries)

Overall System Mood: ANXIOUS

The air feels a bit tense. Some warnings are present, but no critical failures yet. Keep an eye on things!
```

## Development

This utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

To ensure the analyzer is working as expected, run the provided tests:

```bash
python -m unittest tests/test_analyzer.py
```
