# Cosmic Dust Collector

## 🌌 Sweep Away Digital Debris with Whimsical Precision!

The Cosmic Dust Collector is a Python utility designed to help you maintain a pristine digital environment by identifying and optionally cleaning up 'cosmic dust' – those pesky temporary files, ancient log entries, and desolate empty directories that accumulate over time.

Think of it as your personal digital janitor, but with a flair for the cosmic!

## ✨ Features

*   **Temporary File Detection**: Scans for files matching common temporary extensions (`.tmp`, `.log`, `.bak`, `.swp`, etc.) that are older than a specified age.
*   **Empty Directory Identification**: Pinpoints directories that contain no files or only other empty directories, ready for collapse.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Actual Cleanup Mode**: Confidently remove identified dust with a single command.
*   **Configurable**: Customize age thresholds, temporary file extensions, and exclusion patterns.

## 🚀 Usage

To use the Cosmic Dust Collector, simply run the `collector.py` script with your desired arguments.

```bash
python utils/cosmic-dust-collector/src/collector.py [path] [options]
```

### Examples:

1.  **Scan current directory (dry run, default settings):**
    ```bash
    python utils/cosmic-dust-collector/src/collector.py
    ```

2.  **Scan a specific directory (`/var/log`) for dust older than 60 days (dry run):**
    ```bash
    python utils/cosmic-dust-collector/src/collector.py /var/log --age 60
    ```

3.  **Perform actual cleanup in your home directory, considering `.cache` and `node_modules` as exclusions:**
    ```bash
    python utils/cosmic-dust-collector/src/collector.py ~/ --clean --exclude .cache node_modules
    ```

4.  **Scan with custom temporary extensions (e.g., only `.temp` and `.old` files):**
    ```bash
    python utils/cosmic-dust-collector/src/collector.py --extensions .temp .old
    ```

### Arguments:

*   `path`: The path to scan for cosmic dust (default: current directory `.`)
*   `--age <int>`: Minimum age in days for temporary files to be considered dust (default: `30`)
*   `--extensions <ext1> <ext2> ...`: List of file extensions to consider as temporary (default: `.tmp .log .bak .swp .temp .old`)
*   `--exclude <pattern1> <pattern2> ...`: List of path patterns to exclude from scanning (e.g., `node_modules`, `.git`)
*   `--clean`: Perform actual cleanup (delete files/directories). By default, it's a dry run.

## 🧪 Testing

To ensure the Cosmic Dust Collector is always ready for its celestial duties, run the provided unit tests:

```bash
python utils/cosmic-dust-collector/tests/test_collector.py
```

The tests use `unittest.mock` to simulate file system interactions, ensuring deterministic and offline validation of the utility's logic without touching your actual files.
