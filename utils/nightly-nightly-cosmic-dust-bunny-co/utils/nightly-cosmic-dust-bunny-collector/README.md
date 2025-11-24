# Nightly Cosmic Dust Bunny Collector

## 🌌 Purpose

The digital cosmos can get cluttered with forgotten files, temporary detritus, and ancient logs – what we affectionately call "Cosmic Dust Bunnies." This utility helps you identify these digital relics, providing a clear report so you can decide which ones to sweep away and which to cherish (for some reason). It's your personal digital broom for a tidier system!

## ✨ Features

*   **Directory Scanning**: Recursively scans specified directories for potential "dust bunnies."
*   **Age-Based Detection**: Identifies files older than a configurable number of days.
*   **Extension Filtering**: Can target specific file extensions (e.g., `.tmp`, `.log`, `.bak`).
*   **Empty Directory Spotting**: Finds and reports empty directories.
*   **Detailed Reporting**: Provides a clear, categorized list of identified items.

## 🚀 Usage

### Prerequisites

*   Python 3.8+ (standard library only)

### Running the Collector

1.  Navigate to the `nightly-cosmic-dust-bunny-collector` directory.
2.  Run the `collector.py` script with the desired paths and options:

    ```bash
    python src/collector.py --path /path/to/scan1 --path /path/to/scan2 --age 30 --extensions .tmp .log --report-empty-dirs
    ```

    *   `--path <directory>`: (Required, can be specified multiple times) The directory to scan.
    *   `--age <days>`: (Optional, default: 30) Report files older than this many days.
    *   `--extensions <ext1> <ext2> ...`: (Optional) Report files with these specific extensions, regardless of age. Extensions are case-insensitive.
    *   `--report-empty-dirs`: (Optional) Include empty directories in the report.
    *   `--output <file>`: (Optional) Save the report to a file instead of printing to console.

### Example

```bash
python src/collector.py --path ~/Downloads --path /var/log --age 90 --extensions .bak .old --report-empty-dirs
```

This command will scan your `Downloads` folder and `/var/log`, looking for files older than 90 days, any files ending in `.bak` or `.old` (case-insensitive), and any empty directories.

## 🧪 Testing

To ensure our cosmic broom is working correctly, run the tests:

```bash
python -m unittest tests/test_collector.py
```
