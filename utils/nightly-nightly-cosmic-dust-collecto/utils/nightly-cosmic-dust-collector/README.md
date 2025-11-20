# Nightly Cosmic Dust Collector

The digital universe accumulates "cosmic dust" – forgotten, tiny, or ancient files that clutter your repository and obscure important artifacts. The Nightly Cosmic Dust Collector is your automated janitor, designed to identify and report these digital specks so you can decide whether to sweep them away or cherish them as historical relics.

## Features

*   Scans specified directories for files matching criteria.
*   Identifies files older than a configurable age.
*   Flags files smaller than a configurable size (including empty files).
*   Allows filtering by file extension (include/exclude lists).
*   Provides a clear report of identified "dust" for manual review.

## Usage

```bash
python3 src/dust_collector.py --path <directory_to_scan> [OPTIONS]
```

### Arguments

*   `--path <directory>`: **Required**. The root directory to start scanning from.
*   `--min-age-days <int>`: Files older than this many days will be considered "dust". Default: `30`.
*   `--max-size-kb <int>`: Files smaller than this many kilobytes (KB) will be considered "dust". Default: `10`.
*   `--include-ext <.ext1,.ext2>`: Comma-separated list of file extensions to *include* in the scan (e.g., `.log,.tmp`). If empty, all extensions are considered.
*   `--exclude-ext <.ext1,.ext2>`: Comma-separated list of file extensions to *exclude* from the scan (e.g., `.py,.md`).

### Example

Scan the current directory for files older than 60 days and smaller than 5KB, excluding Python files:

```bash
python3 src/dust_collector.py --path . --min-age-days 60 --max-size-kb 5 --exclude-ext .py
```

Scan the `logs/` directory for `.log` files older than 7 days:

```bash
python3 src/dust_collector.py --path logs/ --min-age-days 7 --include-ext .log
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.
