# Digital Dust Bunny Sweeper

## Overview

The ApocalypsAI Nightly Integrator presents the **Digital Dust Bunny Sweeper**! In these uncertain times, digital clutter can be as overwhelming as physical debris. This whimsical yet practical utility helps you identify and report 'digital dust bunnies' – those forgotten, old, or empty files and directories that silently accumulate, consuming precious disk space and mental bandwidth.

Think of it as a digital spring cleaning tool, designed to bring order to your filesystem chaos before the real chaos descends.

## Features

*   **Age-based Detection**: Finds files and directories older than a specified threshold.
*   **Empty Directory Identification**: Pinpoints and reports empty folders.
*   **Pattern Matching**: Allows inclusion and exclusion of files based on glob patterns.
*   **Report-Only Mode**: Safely lists potential dust bunnies without deleting anything, giving you full control.

## Installation

This utility is self-contained. No special installation steps are required beyond having Python 3.6+ installed.

## Usage

Run the `sweeper.py` script directly from its directory.

```bash
python src/sweeper.py --path /path/to/scan --age 30 --include "*.log" "*.tmp" --exclude "*.git" "node_modules"
```

### Arguments:

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--age <days>` (optional, default: 365): Files/directories older than this many days will be flagged.
*   `--include <pattern> [<pattern>...]` (optional): Glob patterns for files/directories to *include* in the scan (e.g., `*.log`, `temp_*`). Can be specified multiple times.
*   `--exclude <pattern> [<pattern>...]` (optional): Glob patterns for files/directories to *exclude* from the scan (e.g., `*.bak`, `node_modules`). Can be specified multiple times.
*   `--dry-run` (optional, default: True): If set, only reports findings without performing any deletion. Currently, this utility *only* reports.

## Example Output

```
Scanning /home/user/documents for digital dust bunnies...

Found 3 digital dust bunnies:

- /home/user/documents/old_logs/archive.log (File, 450 days old)
- /home/user/documents/temp_files/ (Empty Directory)
- /home/user/documents/drafts/abandoned_project.txt (File, 90 days old)

Scan complete. No actual deletion performed (dry-run mode).
```

## Development

To run tests:

```bash
python -m unittest tests/test_sweeper.py
```
