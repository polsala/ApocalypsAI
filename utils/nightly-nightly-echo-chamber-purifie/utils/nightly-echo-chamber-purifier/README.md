# Nightly Echo Chamber Purifier

## 🌌 Purpose

The Nightly Echo Chamber Purifier is a whimsical-yet-useful utility designed to help you maintain a pristine digital environment by identifying and reporting duplicate files within a specified directory. Like a cosmic janitor, it sweeps through your file system, detecting redundant "echoes" of data that consume valuable space and clutter your digital landscape.

## ✨ Features

*   **Duplicate Detection**: Scans a given directory (and its subdirectories) for files with identical content.
*   **Hashing Algorithms**: Supports MD5 (default), SHA1, and SHA256 for robust content comparison.
*   **Clear Reporting**: Presents duplicate files grouped by their content hash, making it easy to identify and manage redundant data.
*   **Self-contained**: A single Python script with minimal dependencies, ready to run.

## 🚀 How to Use

1.  **Navigate**: Change into the `src` directory:
    ```bash
    cd utils/nightly-echo-chamber-purifier/src
    ```

2.  **Run**: Execute the `purifier.py` script, providing the target directory you wish to scan.

    ```bash
    python purifier.py /path/to/your/target/directory
    ```

    **Example**: Scan your `Downloads` folder for duplicates:
    ```bash
    python purifier.py ~/Downloads
    ```

3.  **Specify Hashing Algorithm (Optional)**: You can choose a different hashing algorithm using the `--hash-algo` flag:
    ```bash
    python purifier.py /path/to/your/target/directory --hash-algo sha256
    ```
    Available algorithms: `md5`, `sha1`, `sha256`.

## 🧪 How to Test

1.  **Navigate**: Change into the `tests` directory:
    ```bash
    cd utils/nightly-echo-chamber-purifier/tests
    ```

2.  **Run Tests**: Execute the Python unit tests:
    ```bash
    python -m unittest test_purifier.py
    ```

    This will run all defined tests, ensuring the duplicate detection logic works as expected without touching your actual file system.

## 🛠️ Development Notes

*   **Language**: Python 3.11+
*   **Dependencies**: Standard library only (`os`, `hashlib`, `argparse`, `collections`).
*   **Self-Contained**: Designed to be run directly without complex setup.
