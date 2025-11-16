# Nightly Cosmic Dust Collector

## Purpose

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a clean and tidy repository. It scans designated directories for files that might be considered 'cosmic dust' – specifically, files that are very small, very old, or completely empty. These files often accumulate as temporary artifacts, forgotten logs, or remnants of past development, contributing to repository clutter.

This utility identifies such files and can either report them for manual review or automatically move them to a specified 'quarantine' directory, allowing for a more organized and efficient workspace.

## Usage

```bash
python src/dust_collector.py --path <directory_to_scan> \
                            [--quarantine-dir <quarantine_path>] \
                            [--max-size-kb <size_in_kb>] \
                            [--min-age-days <age_in_days>] \
                            [--report-only]
```

### Arguments:

*   `--path <directory_to_scan>`: **Required**. The root directory to start scanning for dust.
*   `--quarantine-dir <quarantine_path>`: **Optional**. If provided, identified 'dust' files will be moved here. If not provided, files will only be reported.
*   `--max-size-kb <size_in_kb>`: **Optional**. Maximum file size in kilobytes to consider as dust. Defaults to 1 KB (1024 bytes).
*   `--min-age-days <age_in_days>`: **Optional**. Minimum age in days for a file to be considered dust. Defaults to 30 days.
*   `--report-only`: **Optional**. If set, files will only be reported, even if `--quarantine-dir` is specified. This overrides the move action.

## Examples

1.  **Report all dust files older than 60 days and smaller than 0.5KB in the current directory:**
    ```bash
    python src/dust_collector.py --path . --min-age-days 60 --max-size-kb 0.5 --report-only
    ```

2.  **Move all dust files (default criteria) from `temp/` to `quarantine/`:**
    ```bash
    python src/dust_collector.py --path temp/ --quarantine-dir quarantine/
    ```

3.  **Find empty files in `logs/` and report them:**
    ```bash
    python src/dust_collector.py --path logs/ --max-size-kb 0.001 --report-only # 0.001KB is effectively 0 bytes
    ```

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No special installation needed. Just run the script.
python src/dust_collector.py --help
```
