# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help keep your repository clean and free of digital 'dust'. It scans specified directories for files that meet certain criteria (e.g., very small files, temporary files, old logs) and offers options to either list them or move them to a designated 'quarantine' folder for later review or deletion.

Think of it as a tiny, automated janitor for your digital space, sweeping away the forgotten bits and bytes that accumulate over time.

## Features

*   **Configurable Size Threshold**: Identify files smaller than a specified size.
*   **Extension Filtering**: Optionally target files with specific extensions (e.g., `.log`, `.tmp`, `.bak`).
*   **List Mode**: Preview the 'dust' without making any changes.
*   **Quarantine Mode**: Safely move identified files to a dedicated 'quarantine' directory, preserving their relative path structure.

## Installation

This utility is self-contained. Simply place the `nightly-cosmic-dust-collector` folder within your `utils/` directory.

## Usage

Run the `dust_collector.py` script from your terminal.

```bash
python3 src/dust_collector.py --help
```

### Examples:

1.  **List all files smaller than 1KB in the current directory and its subdirectories:**

    ```bash
    python3 src/dust_collector.py --path . --size 1024 --mode list
    ```

2.  **Move all `.log` and `.tmp` files smaller than 5KB from the `logs/` directory to a `quarantine/` folder:**

    ```bash
    python3 src/dust_collector.py --path logs/ --size 5120 --extensions .log .tmp --mode quarantine --quarantine-dir .dust_quarantine
    ```

3.  **List all files smaller than 100 bytes in the entire repository (from root):**

    ```bash
    python3 src/dust_collector.py --path ../../ --size 100 --mode list
    ```

## Arguments

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--size <bytes>` (optional, default: 1024): Maximum file size in bytes to consider as 'dust'.
*   `--extensions <ext1> <ext2> ...` (optional): Space-separated list of file extensions (e.g., `.log .tmp`) to include. If not specified, all files matching the size criteria are considered.
*   `--mode <list|quarantine>` (optional, default: `list`): Operation mode. `list` will print files; `quarantine` will move them.
*   `--quarantine-dir <directory>` (optional, default: `quarantine_dust`): Directory to move files to in `quarantine` mode. Will be created if it doesn't exist.

## Development

To run tests:

```bash
python3 -m unittest tests/test_dust_collector.py
```
