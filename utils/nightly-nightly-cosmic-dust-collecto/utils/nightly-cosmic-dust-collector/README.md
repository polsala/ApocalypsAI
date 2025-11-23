# 🌌 Nightly Cosmic Dust Collector

Welcome, intrepid space-cleaner! The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you tidy up your digital cosmos. It scans specified directories for files that might be considered 'cosmic dust' – typically small, old, or empty files that accumulate over time and contribute to digital clutter.

Think of it as your personal orbital vacuum cleaner, identifying forgotten remnants that might be ripe for review or deletion, freeing up precious storage and mental space.

## ✨ Features

*   **Size-based Filtering**: Identify files smaller than a configurable maximum size.
*   **Age-based Filtering**: Pinpoint files older than a specified number of days.
*   **Empty File Detection**: Optionally include or exclude completely empty files.
*   **Directory Exclusion**: Skip over known noisy directories like `.git` or `node_modules`.
*   **Clear Reporting**: Provides a list of identified 'dust' files with their paths, sizes, and ages.

## 🚀 Usage

To run the Cosmic Dust Collector, navigate to its directory and execute the `dust_collector.py` script with the target path.

```bash
python3 src/dust_collector.py <path_to_scan> [options]
```

### Arguments

*   `<path_to_scan>`: The root directory where the cosmic dust collection should begin.

### Options

*   `--max-size <KB>`: Maximum file size in Kilobytes to consider as dust. Files larger than this will be ignored. (Default: `1024` KB / 1 MB)
*   `--min-age <days>`: Minimum age in days for a file to be considered dust. Files newer than this will be ignored. (Default: `30` days)
*   `--no-empty`: If present, empty files (0 bytes) will NOT be included in the dust collection, even if they meet age and size criteria.
*   `--exclude-dirs <dir1> <dir2> ...`: A space-separated list of directory names to completely exclude from the scan. Useful for skipping dependency folders or version control directories. (e.g., `.git node_modules build`)

## 🌠 Examples

1.  **Scan your current directory for default dust (small, older than 30 days, includes empty):**
    ```bash
    python3 src/dust_collector.py .
    ```

2.  **Find files smaller than 500KB and older than 90 days in your 'documents' folder, excluding empty files:**
    ```bash
    python3 src/dust_collector.py ~/documents --max-size 500 --min-age 90 --no-empty
    ```

3.  **Scan a project directory, ignoring `.git` and `venv` folders:**
    ```bash
    python3 src/dust_collector.py ~/my_project --exclude-dirs .git venv
    ```

## 🧹 Output

The utility will print a report to the console, listing each identified 'dust' file with its details. If no dust is found, it will let you know!

```
🌌 Cosmic Dust Report for '/home/user/my_project':
- Path: /home/user/my_project/old_temp.log
  Size: 123 bytes
  Last Modified: 2023-01-15T10:30:00 (60.5 days old)
--------------------
- Path: /home/user/my_project/subdir/forgotten_note.txt
  Size: 50 bytes
  Last Modified: 2023-02-01T14:00:00 (43.2 days old)
--------------------

Total 2 dust particles collected.
```

May your digital space be ever clean and your cosmic journey unburdened!
