# Cosmic Dust Bunny Collector

## 🌌 Overview

The `Cosmic Dust Bunny Collector` is a whimsical yet practical utility designed to help you maintain a pristine digital environment. Over time, our file systems accumulate "dust bunnies" – old, forgotten, empty, or temporary files that clutter space and obscure important data. This tool helps you identify these digital remnants, making it easier to decide what to keep and what to jettison into the void.

Think of it as your personal space janitor, scanning your directories for cosmic debris!

## ✨ Features

*   **Age-based Detection**: Flag files older than a specified number of days.
*   **Empty File Identification**: Pinpoint zero-byte files that serve no purpose.
*   **Pattern Matching**: Locate files by simple glob-like patterns (e.g., `*.tmp`, `backup.*`).
*   **Recursive Scanning**: Dives deep into subdirectories to find hidden dust bunnies.
*   **Clear Reporting**: Presents findings in an easy-to-read format, categorizing the detected files.

## 🚀 Usage

The `cosmic-dust-bunny-collector` is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or newer.

### Running the Collector

Navigate to the `utils/cosmic-dust-bunny-collector/` directory and run the `collector.py` script directly.

```bash
python src/collector.py <directory_to_scan> [options]
```

### Arguments

*   `<directory_to_scan>`: The path to the directory you wish to scan. This is a required argument.

### Options

*   `--max-age <days>`: Files older than this many days will be flagged as 'old'. Default is `30` days.
    *   Example: `--max-age 90` to find files older than 90 days.
*   `--include-empty`: Use this flag to include empty (zero-byte) files in the scan results.
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of file patterns to match. Supports simple glob-like matching with `*` at the start or end (e.g., `*.tmp`, `backup.*`, `error.log`).
    *   Example: `--patterns "*.log" "*.bak" "temp_file.txt"`

### Examples

1.  **Scan current directory for files older than 60 days:**
    ```bash
    python src/collector.py . --max-age 60
    ```

2.  **Scan a specific project directory for empty files and files ending with `.tmp` or starting with `cache_`:**
    ```bash
    python src/collector.py /path/to/my/project --include-empty --patterns "*.tmp" "cache_*"
    ```

3.  **Find all types of dust bunnies (old, empty, and specific patterns) in your home directory:**
    ```bash
    python src/collector.py ~/ --max-age 180 --include-empty --patterns "*.old" "*.bak" "debug.log"
    ```

## 🧪 Testing

To run the tests for the Cosmic Dust Bunny Collector, navigate to the utility's root directory and execute the `unittest` module:

```bash
python -m unittest tests/test_collector.py
```

All tests are designed to be deterministic and run offline using `unittest.mock` to simulate file system interactions.

## 📜 License

This utility is released under the [MIT License](LICENSE).
