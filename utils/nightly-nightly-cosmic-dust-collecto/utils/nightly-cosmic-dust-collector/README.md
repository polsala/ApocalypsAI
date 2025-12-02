# Nightly Cosmic Dust Collector

## 🌌 What is the Cosmic Dust Collector?

In the vast expanse of your project directories, 'cosmic dust' accumulates: old log files, forgotten temporary data, stale backups, and other digital detritus. The Nightly Cosmic Dust Collector is a whimsical-yet-powerful utility designed to help you identify and manage this digital clutter. It scans specified directories for files that meet certain criteria (e.g., older than a certain age, matching specific patterns) and can optionally move them to a designated 'archive' folder, keeping your active workspace pristine.

## ✨ Features

*   **Age-based Collection**: Identify files older than a specified number of days.
*   **Pattern Matching**: Target specific file types or names using glob patterns (e.g., `*.log`, `temp_*`).
*   **Archiving**: Automatically move identified 'dust' files to an `archive` subdirectory within the target directory.
*   **Dry Run Mode**: Preview which files would be collected without making any changes.
*   **Self-contained**: A single Python script with minimal dependencies.

## 🚀 Usage

To run the Cosmic Dust Collector, navigate to its directory and execute the `dust_collector.py` script. 

```bash
python src/dust_collector.py --help
```

### Basic Collection (Dry Run)

To see what files would be collected in the current directory that are older than 30 days, without moving them:

```bash
python src/dust_collector.py --target-dir . --age 30
```

### Archiving Old Logs

To move all `.log` files older than 60 days from `/var/log/my_app` to an `archive` subdirectory within `/var/log/my_app`:

```bash
python src/dust_collector.py --target-dir /var/log/my_app --age 60 --patterns "*.log" --archive
```

### Collecting Temporary Files

To collect any file matching `*.tmp` or `temp_*` older than 7 days in your home directory, and archive them:

```bash
python src/dust_collector.py --target-dir ~/my_project --age 7 --patterns "*.tmp" "temp_*" --archive
```

### Arguments

*   `--target-dir <path>`: The directory to scan for cosmic dust. (Required)
*   `--age <days>`: Files older than this many days will be considered dust. (Default: 30)
*   `--patterns <pattern1> [<pattern2> ...]`: One or more glob patterns to match filenames (e.g., `*.log`, `temp_*`). If not provided, all files are considered.
*   `--archive`: If set, identified files will be moved to an `archive` subdirectory within the `target-dir`. Otherwise, it's a dry run.

## 🛠️ Development

The utility is written in Python 3.11 and uses standard library modules. Tests are located in the `tests/` directory and can be run using `unittest`.

```bash
python -m unittest tests/test_dust_collector.py
```
