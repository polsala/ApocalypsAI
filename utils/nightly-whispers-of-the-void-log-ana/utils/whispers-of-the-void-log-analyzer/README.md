# Whispers of the Void Log Analyzer

## Overview

The "Whispers of the Void Log Analyzer" is a whimsical-yet-critical utility designed to help you detect early signs of impending digital doom within your system logs. Instead of waiting for a full-blown apocalypse, this tool scans your log files for configurable "premonitions" – specific keywords or regular expressions that hint at future calamities. Think of it as a digital oracle, sifting through the noise to find the subtle whispers of the void.

## Features

*   **Configurable Premonitions**: Define your own keywords and regular expressions to identify potential issues.
*   **Line-by-Line Scanning**: Efficiently processes log files, reporting all matches with their line numbers.
*   **Self-Contained**: A single Python script with minimal dependencies, easy to integrate into any monitoring setup.

## Installation

This utility is self-contained. No special installation steps are required beyond having Python 3.6+ installed.

## Usage

To run the analyzer, simply execute the `analyzer.py` script with your log file and an optional configuration file.

```bash
python src/analyzer.py <path_to_log_file> [--config <path_to_config_file>]
```

### Arguments:

*   `<path_to_log_file>`: **Required**. The path to the log file you want to analyze.
*   `--config <path_to_config_file>`: **Optional**. The path to a JSON configuration file defining your "premonitions." If not provided, a default set of common error keywords will be used.

### Example:

```bash
# Using default premonitions
python src/analyzer.py /var/log/syslog

# Using a custom configuration
python src/analyzer.py /var/log/nginx/error.log --config my_doom_config.json
```

## Configuration File (`my_doom_config.json`)

The configuration file is a JSON file that specifies the keywords and regular expressions to look for.

```json
{
    "keywords": [
        "error",
        "fail",
        "critical",
        "denied",
        "out of memory",
        "disk full",
        "unreachable"
    ],
    "regexes": [
        "^(CRITICAL|EMERGENCY):.*",
        "connection reset by peer",
        "segmentation fault",
        "panic:.*"
    ]
}
```

*   `keywords`: A list of strings. The analyzer will look for exact matches (case-insensitive) of these keywords within each log line.
*   `regexes`: A list of regular expression strings. The analyzer will attempt to match these patterns against each log line.

## Output

The script will print any detected "premonitions" to standard output, indicating the line number and the matched pattern.

```
[LINE 15] Premonition: 'disk full'
[LINE 28] Premonition: Regex '^(CRITICAL|EMERGENCY):.*' matched 'CRITICAL: Database connection lost!'
[LINE 102] Premonition: 'fail'
```
