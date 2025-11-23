# Nightly Digital Debris Sweeper

## 🧹 Overview

The Nightly Digital Debris Sweeper is a whimsical-yet-useful utility designed to help keep your digital landscape pristine. After the daily "apocalypse" (or just regular system operations), temporary files, old logs, and forgotten backups can accumulate, cluttering your storage and potentially hiding critical information. This tool scans specified directories to identify and report such "digital debris" based on age or file patterns, allowing you to review and clean up your system effectively.

Think of it as a diligent janitor for your file system, ensuring no digital dust bunnies or forgotten relics linger too long.

## ✨ Features

*   **Age-Based Scanning**: Identify files older than a specified number of days.
*   **Pattern-Based Scanning**: Locate files matching common temporary or backup patterns (e.g., `.tmp`, `.bak`, `.log.old`).
*   **Recursive Directory Scan**: Traverses subdirectories to find hidden debris.
*   **Clear Reporting**: Outputs a list of identified debris files, ready for review.
*   **Self-Contained**: Written in Python, with minimal dependencies, making it easy to run anywhere.

## 🚀 Usage

### Prerequisites

*   Python 3.x

### Running the Sweeper

Navigate to the `utils/nightly-digital-debris-sweeper` directory.

```bash
python src/sweeper.py <directory_to_scan> [OPTIONS]
```

**Arguments:**

*   `<directory_to_scan>`: The root directory where the sweeper will start looking for debris. This is a required positional argument.

**Options:**

*   `--age <days>`: Files older than this many days will be considered debris. Default is `30`. Set to `0` to disable age-based filtering.
    *   Example: `--age 7` (finds files older than 7 days)
*   `--patterns <pattern1,pattern2,...>`: A comma-separated list of glob-style patterns (e.g., `*.tmp,*.bak,*.log.old`). Files matching any of these patterns will be considered debris. Default is `*.tmp,*.bak,*.log.old`. Set to an empty string (`--patterns ""`) to disable pattern-based filtering.
    *   Example: `--patterns "*.temp,*.old"`

### Examples

1.  **Scan your home directory for files older than 60 days and common temporary files:**
    ```bash
    python src/sweeper.py ~/ --age 60 --patterns "*.tmp,*.bak,*.log.old"
    ```

2.  **Scan a project directory only for files ending with `.swp` or `.DS_Store` (ignoring age):**
    ```bash
    python src/sweeper.py /path/to/my/project --age 0 --patterns "*.swp,.DS_Store"
    ```

3.  **Scan a log directory for any file older than 7 days (ignoring patterns):**
    ```bash
    python src/sweeper.py /var/log --age 7 --patterns ""
    ```

4.  **Perform a default scan on the current directory (30 days age, default patterns):**
    ```bash
    python src/sweeper.py .
    ```

## 🧪 Testing

To run the tests for the Nightly Digital Debris Sweeper, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```

All tests are designed to be deterministic and run offline using Python's `unittest.mock` to simulate file system operations and time.
