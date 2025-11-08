# Codebase Entropy Monitor

## Overview

The `codebase-entropy-monitor` is a vital tool for any repository aiming for long-term survival in the digital wasteland. It acts as an early warning system, scanning your codebase for signs of 'entropy' – the natural tendency of systems to degrade into disorder. By identifying stale files, undocumented code, and overly large files, this utility provides a 'survival report' that highlights areas needing immediate attention to prevent decay and ensure the codebase remains maintainable and resilient.

Think of it as a digital archaeologist, unearthing forgotten artifacts and pointing out structural weaknesses before they lead to catastrophic collapse.

## Features

- **Stale File Detection**: Identifies files that haven't been modified in a configurable number of days, suggesting potential dead code or forgotten components.
- **Undocumented Code Analysis**: Scans Python files for functions and classes lacking docstrings, indicating areas where knowledge transfer is at risk.
- **Large File Identification**: Flags files exceeding a specified line count, which often correlate with increased complexity and reduced maintainability.
- **Comprehensive Survival Report**: Generates a clear, actionable report detailing all detected entropy, categorized for easy review.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No special installation steps needed. Just run the script directly.
# Ensure you have Python 3.8 or newer installed.
```

## Usage

Run the `entropy_monitor.py` script from the command line, providing the path to the codebase you wish to scan.

```bash
python utils/codebase-entropy-monitor/src/entropy_monitor.py <path_to_codebase> [options]
```

### Options:

- `--stale-days <int>`: Minimum number of days a file must be untouched to be considered stale. Default: `90`.
- `--max-file-loc <int>`: Maximum lines of code a file can have before being flagged as large. Default: `500`.
- `--output <path>`: Path to save the report. If not provided, prints to console.

### Example:

```bash
python utils/codebase-entropy-monitor/src/entropy_monitor.py ./my_project --stale-days 180 --max-file-loc 1000 --output entropy_report.txt
```

This will scan `./my_project`, flagging files untouched for 180 days or longer, and files with over 1000 lines of code. The report will be saved to `entropy_report.txt`.

## Development & Testing

Tests are located in `tests/test_entropy_monitor.py` and can be run using `unittest`.

```bash
python -m unittest utils/codebase-entropy-monitor/tests/test_entropy_monitor.py
```
