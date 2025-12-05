# Nightly Echo Chamber Monitor

## Overview
In the vast, echoing chambers of the digital wasteland, redundant data can accumulate like cosmic dust, consuming precious storage and obscuring vital information. The Nightly Echo Chamber Monitor is a standalone utility designed to combat this digital entropy by identifying duplicate files across specified directories.

It scans for files with identical content by calculating their MD5 hash, providing a clear report of all 'echoes' found. This helps maintain a lean, efficient, and well-organized data repository, ensuring that every byte serves a unique purpose.

## Features
-   **Content-Based Duplication Detection**: Uses MD5 hashing to accurately identify files with identical content, regardless of their name or location.
-   **Directory Traversal**: Recursively scans one or more specified directories.
-   **Clear Reporting**: Outputs a list of duplicate files, grouped by their shared content hash.
-   **Self-Contained**: Written in Python 3.11, with no external dependencies beyond the standard library.

## Usage

To run the Echo Chamber Monitor, execute the `echo_monitor.py` script with the paths to the directories you wish to scan:

```bash
python3 src/echo_monitor.py /path/to/directory1 /path/to/another/directory
```

**Example:**

```bash
python3 src/echo_monitor.py ~/documents /var/log/backups
```

If duplicate files are found, the utility will print them to standard output, grouped by their content hash. If no duplicates are found, a message indicating this will be displayed.

### Exit Codes
-   `0`: Duplicates were found and reported.
-   `2`: No duplicate files were found (no-op).
-   `1`: An error occurred during execution (e.g., file access issues).

## Development

The utility is written in Python 3.11. All dependencies are part of the standard library.

### Running Tests
To ensure the Echo Chamber Monitor is functioning correctly, navigate to the `utils/nightly-echo-chamber-monitor` directory and run the tests using `unittest`:

```bash
python3 -m unittest tests/test_echo_monitor.py
```

Tests are designed to be deterministic and run offline using Python's `unittest.mock` library to simulate file system interactions and hash calculations.
