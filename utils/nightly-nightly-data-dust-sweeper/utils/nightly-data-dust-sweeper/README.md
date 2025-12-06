# Nightly Data-Dust Sweeper

## 🧹 Overview

The Nightly Data-Dust Sweeper is a whimsical-yet-useful utility designed to help you keep your digital wasteland tidy. It scans specified directories and files to identify and report duplicate files, which we affectionately call "data-dust." By finding these redundant copies, you can reclaim valuable storage space and maintain a cleaner, more efficient file system.

## ✨ Features

*   **Duplicate Detection**: Identifies files with identical content using cryptographic hashing (MD5, SHA1, SHA256).
*   **Directory Traversal**: Recursively scans entire directories for files.
*   **Multiple Paths**: Accepts multiple file and directory paths as input.
*   **Configurable Hashing**: Choose between MD5, SHA1, or SHA256 for hashing.
*   **Clear Reporting**: Outputs a summary of all duplicate sets found.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+

### Running the Sweeper

1.  Navigate to the `utils/nightly-data-dust-sweeper/` directory.
2.  Run the `sweeper.py` script from your terminal, providing the paths you want to scan.

```bash
python src/sweeper.py <path1> [<path2> ...] [--hash-algo <algorithm>]
```

**Examples:**

*   Scan a single directory:
    ```bash
    python src/sweeper.py /home/user/documents
    ```
*   Scan multiple directories:
    ```bash
    python src/sweeper.py /var/logs /tmp/backups
    ```
*   Scan a mix of files and directories:
    ```bash
    python src/sweeper.py /home/user/report.pdf /mnt/archive/old_docs
    ```
*   Use SHA256 for hashing:
    ```bash
    python src/sweeper.py /my/data --hash-algo sha256
    ```

### Arguments

*   `<path>`: One or more file or directory paths to scan.
*   `--hash-algo <algorithm>`: (Optional) The hashing algorithm to use. Choices are `md5` (default), `sha1`, or `sha256`.

## 🧪 Testing

To run the tests for the Data-Dust Sweeper:

1.  Navigate to the `utils/nightly-data-dust-sweeper/` directory.
2.  Execute the tests using `unittest`:

```bash
python -m unittest tests/test_sweeper.py
```

The tests are designed to be deterministic and do not interact with the actual file system, using mocks to simulate file operations.

## 🤝 Contributing

Feel free to suggest improvements or report issues!
