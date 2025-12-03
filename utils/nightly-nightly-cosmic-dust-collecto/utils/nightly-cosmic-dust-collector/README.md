# Nightly Cosmic Dust Collector

## 🌌 Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you declutter your digital cosmos. It scans a specified directory for "cosmic dust" – empty folders and files smaller than a configurable size – and offers to sweep them away, freeing up precious digital space. Keep your repository, project folders, or even your entire system clean and pristine!

## ✨ Features

*   **Dust Detection**: Identifies empty directories and files below a specified size threshold.
*   **Configurable Size**: Define what constitutes "dust" by setting a minimum file size in bytes.
*   **Dry Run Mode**: Preview what would be removed without making any actual changes, ensuring peace of mind.
*   **Actual Collection**: Safely remove identified dust to reclaim disk space.
*   **Detailed Report**: Provides a summary of all files and directories identified or removed.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Collector

Navigate to the `src` directory within the `nightly-cosmic-dust-collector` folder and run `collector.py` from your terminal:

```bash
cd utils/nightly-cosmic-dust-collector/src
python collector.py <target_directory> [options]
```

**Arguments:**

*   `<target_directory>`: The path to the directory you want to scan and clean.

**Options:**

*   `--min-file-size <bytes>`: Files smaller than this size (in bytes) will be considered "dust". Default is `1` byte (i.e., empty files).
*   `--dry-run`: Perform a dry run. The utility will report what *would* be removed without actually deleting anything. This is highly recommended for a first pass!

### Examples

1.  **Dry run to see all empty files and folders:**
    ```bash
    python collector.py /path/to/your/project --dry-run
    ```

2.  **Dry run to see files smaller than 100 bytes and empty folders:**
    ```bash
    python collector.py /path/to/your/downloads --min-file-size 100 --dry-run
    ```

3.  **Actually remove empty files and folders (use with caution!):**
    ```bash
    python collector.py /path/to/your/temp_files
    ```
    (This uses the default `min-file-size` of 1 byte and performs actual removal as `--dry-run` is not specified.)

4.  **Actually remove files smaller than 50 bytes and empty folders:**
    ```bash
    python collector.py /path/to/your/cache --min-file-size 50
    ```

## 🧪 Testing

To run the tests, navigate to the `tests` directory and execute the Python test runner:

```bash
cd utils/nightly-cosmic-dust-collector/tests
python -m unittest test_collector.py
```

The tests are designed to be deterministic and offline, using temporary directories and mocking `os.path.getsize` to simulate various file sizes without actual disk writes affecting test outcomes.
