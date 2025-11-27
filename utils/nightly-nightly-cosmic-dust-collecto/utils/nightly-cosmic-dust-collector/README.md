# Nightly Cosmic Dust Collector

## Overview

The ApocalypsAI Nightly Cosmic Dust Collector is a utility designed to help keep your project directories tidy and free from digital clutter. It identifies files that are likely forgotten, temporary, or simply taking up space without purpose, affectionately termed 'cosmic dust'.

This utility can detect:

1.  **Empty Files**: Files with zero bytes.
2.  **Aged Small Files**: Files older than a specified number of days and smaller than a certain size threshold.
3.  **Temporary Pattern Files**: Files matching common temporary patterns (e.g., `.tmp`, `~`, `.bak`, `.swp`).

Once identified, these 'dusty' files are reported. In non-dry-run mode, they can be automatically moved to a designated 'quarantine' directory, allowing you to review them before permanent deletion or archival.

## Usage

```bash
python src/dust_collector.py \
  --target-dir /path/to/your/project \
  --quarantine-dir /path/to/quarantine/zone \
  --age-threshold-days 90 \
  --size-threshold-kb 1 \
  --dry-run
```

### Arguments:

*   `--target-dir <path>`: The directory to scan for cosmic dust. (Required)
*   `--quarantine-dir <path>`: The directory where identified dust files will be moved. (Required)
*   `--age-threshold-days <int>`: Files older than this many days (and smaller than `size-threshold-kb`) are considered dust. Default: `90`.
*   `--size-threshold-kb <int>`: Files smaller than this many KB (and older than `age-threshold-days`) are considered dust. Default: `1`.
*   `--dry-run`: If present, the utility will only report files and will not move them. (Optional)

## Examples

**1. Scan and report dust in a project directory (dry run):**

```bash
python src/dust_collector.py \
  --target-dir ./my_repo \
  --quarantine-dir ./dust_quarantine \
  --dry-run
```

**2. Scan and move dust older than 180 days and smaller than 5KB:**

```bash
python src/dust_collector.py \
  --target-dir /var/log/old_logs \
  --quarantine-dir /tmp/log_dust \
  --age-threshold-days 180 \
  --size-threshold-kb 5
```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
