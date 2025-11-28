# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help keep your repository tidy by identifying and managing 'cosmic dust' – those small, old, or empty files that accumulate over time. Think of it as a digital vacuum cleaner for your project, ensuring only relevant files remain.

## Features

*   **Identify Dust**: Scans specified directories for files that meet criteria for 'dust' (e.g., empty, very small, or untouched for a long time).
*   **List Mode**: Simply lists the identified dust files without making any changes.
*   **Archive Mode**: Moves identified dust files to a designated `.cosmic_dust_archive` directory within the scanned root, preserving them for later review.
*   **Delete Mode**: Permanently removes identified dust files.
*   **Configurable**: Thresholds for file size and age can be customized.

## Usage

```bash
python src/dust_collector.py --help
```

### Examples:

1.  **List all cosmic dust in the current directory (default criteria):**
    ```bash
    python src/dust_collector.py list .
    ```

2.  **Archive files older than 180 days and smaller than 500 bytes in 'logs/' directory:**
    ```bash
    python src/dust_collector.py archive logs/ --max-size 500 --max-age 180
    ```

3.  **Delete empty files in 'temp/' directory:**
    ```bash
    python src/dust_collector.py delete temp/ --empty-only
    ```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond standard library modules.

To run, simply navigate to the `utils/nightly-cosmic-dust-collector/` directory and execute the `src/dust_collector.py` script.

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
