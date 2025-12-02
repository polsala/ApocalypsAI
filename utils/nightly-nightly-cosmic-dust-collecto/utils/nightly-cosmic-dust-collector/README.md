# Nightly Cosmic Dust Collector

## 🌌 Overview

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help you maintain a tidy project directory. It scans a specified root directory for 'cosmic dust' – files that are either empty or fall below a certain size threshold. These forgotten files can clutter your workspace, and this tool helps you identify them or move them to a designated 'quarantine' zone for later review.

## ✨ Features

*   **Scan & List**: Identify all files that meet the 'cosmic dust' criteria.
*   **Quarantine**: Safely move identified files to a separate directory, preserving their original relative path structure.
*   **Configurable Threshold**: Define what constitutes 'dust' by setting a maximum file size.

## 🚀 Usage

### Prerequisites

*   Python 3.6+

### Installation (Self-contained)

No installation is required. Simply place the `nightly-cosmic-dust-collector` folder in your `utils/` directory and run the `dust_collector.py` script directly.

### Command Line Interface

```bash
python utils/nightly-cosmic-dust-collector/src/dust_collector.py --help
```

```
usage: dust_collector.py [-h] --path PATH [--threshold THRESHOLD] [--action {list,quarantine}] [--quarantine-dir QUARANTINE_DIR]

Collects cosmic dust (small/empty files) from a directory.

options:
  -h, --help            show this help message and exit
  --path PATH           The root directory to scan for cosmic dust.
  --threshold THRESHOLD
                        Maximum file size in bytes to be considered cosmic dust (default: 1024 bytes).
  --action {list,quarantine}
                        Action to perform: 'list' files or 'quarantine' them (default: list).
  --quarantine-dir QUARANTINE_DIR
                        Directory to move cosmic dust files into when action is 'quarantine'. Required for 'quarantine' action.
```

### Examples

1.  **List all files smaller than 500 bytes in the current directory:**

    ```bash
    python utils/nightly-cosmic-dust-collector/src/dust_collector.py --path . --threshold 500 --action list
    ```

2.  **Quarantine files smaller than 1KB in a specific project directory to a `_quarantine` folder:**

    ```bash
    python utils/nightly-cosmic-dust-collector/src/dust_collector.py --path /path/to/my/project --threshold 1024 --action quarantine --quarantine-dir /path/to/my/project/_quarantine
    ```

3.  **List all empty files (threshold 0) in a subdirectory:**

    ```bash
    python utils/nightly-cosmic-dust-collector/src/dust_collector.py --path my_data/temp --threshold 0 --action list
    ```

## 🧪 Development & Testing

To run the tests for this utility, navigate to the `utils/nightly-cosmic-dust-collector` directory and execute:

```bash
python -m unittest tests/test_dust_collector.py
```

All tests are self-contained and use mocks to ensure determinism and offline execution.
