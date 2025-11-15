# Digital Dust Bunny Sweeper

## 🧹 Overview

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you tidy up your digital abode! It scans specified directories to identify those pesky "digital dust bunnies" – files that are excessively large, ancient, or simply duplicates taking up precious space. Think of it as a friendly robot vacuum for your file system, but instead of sucking up lint, it reports on digital clutter.

## ✨ Features

*   **Giant File Detection**: Finds files exceeding a configurable size threshold.
*   **Ancient File Discovery**: Uncovers files older than a specified age.
*   **Duplicate File Spotting**: Identifies identical files using content hashing.
*   **Report Generation**: Outputs a clear, categorized report of all identified "dust bunnies".
*   **Dry Run Mode**: Always safe, it only reports, never deletes.

## 🚀 Usage

### Prerequisites

*   Python 3.8+

### Installation

No installation needed! Just place the `digital-dust-bunny-sweeper` folder in your `utils/` directory.

### Running the Sweeper

Navigate to the `src` directory and run `sweeper.py` with your desired options:

```bash
python sweeper.py <directory_to_scan> [--max-size <bytes>] [--max-age <days>] [--find-duplicates]
```

**Arguments:**

*   `<directory_to_scan>`: The path to the directory you want to sweep. (Required)
*   `--max-size <bytes>`: Report files larger than this size (in bytes). Default: 100MB (104857600 bytes).
*   `--max-age <days>`: Report files older than this many days. Default: 365 days.
*   `--find-duplicates`: Enable duplicate file detection. This can be CPU-intensive for large directories.

**Example:**

```bash
python sweeper.py /home/user/documents --max-size 52428800 --max-age 180 --find-duplicates
```
This command will scan `/home/user/documents`, report files larger than 50MB, older than 180 days, and any duplicates found.

## 📜 Output Report

The sweeper will print a categorized report to the console, detailing:
*   **Giant Files**: List of files exceeding the size threshold.
*   **Ancient Files**: List of files older than the age threshold.
*   **Duplicate Files**: Groups of identical files.

Each entry will include relevant information like file path, size, and modification date.

## 🧪 Development & Testing

To run the tests, navigate to the `tests` directory and execute `pytest` (if installed) or run the test file directly:

```bash
python -m unittest test_sweeper.py
```

The tests are designed to be deterministic and offline, using mocks for file system operations.
