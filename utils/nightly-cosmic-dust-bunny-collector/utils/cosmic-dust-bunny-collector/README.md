# Cosmic Dust Bunny Collector

## 🌌 Unclutter Your Digital Cosmos! 🌌

In the vast expanse of your digital universe, tiny, forgotten files accumulate like cosmic dust bunnies, slowing down your system and obscuring your important data. The **Cosmic Dust Bunny Collector** is here to help you sweep away these ancient relics before they cause a digital singularity!

This whimsical-yet-useful utility identifies and optionally removes or quarantines files that haven't been touched in a specified period, helping you maintain a pristine and efficient digital environment.

## ✨ Features

*   **Age-based Detection**: Easily find files older than a configurable number of days.
*   **Recursive Scanning**: Dive deep into subdirectories to uncover hidden dust bunnies.
*   **Dry Run Mode**: Preview which files will be affected before making any changes.
*   **Quarantine Option**: Move old files to a designated "quarantine zone" instead of permanent deletion, for a second chance at life.
*   **Simple CLI**: Easy to use from your terminal.

## 🚀 Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having a compatible Python interpreter.

1.  Navigate to the `utils/cosmic-dust-bunny-collector/` directory.
2.  You can run it directly using `python src/collector.py`.

## 🛠️ Usage

Run the collector from the `utils/cosmic-dust-bunny-collector/` directory:

```bash
python src/collector.py <target_directory> [options]
```

### Arguments

*   `<target_directory>`: The path to the directory you want to scan for cosmic dust bunnies.

### Options

*   `--age <days>`: Files older than this many days will be considered dust bunnies. Default is `90` days.
*   `--no-dry-run`: **WARNING**: Use this flag to perform actual file operations (move/delete). By default, the utility runs in dry-run mode, only listing files without making changes.
*   `--recursive`: Scan subdirectories recursively for dust bunnies.
*   `--quarantine <directory_path>`: Move identified files to this directory instead of deleting them. If the directory doesn't exist, it will be created. This option overrides `--no-dry-run` to perform a move operation.

### Examples

1.  **Dry run to see old files in your `downloads` folder (older than 180 days):**
    ```bash
    python src/collector.py ~/Downloads --age 180
    ```

2.  **Recursively find and delete old files in your `temp` directory (older than 30 days):**
    ```bash
    python src/collector.py /tmp --age 30 --recursive --no-dry-run
    ```

3.  **Move old log files (older than 365 days) to a quarantine folder:**
    ```bash
    python src/collector.py /var/log --age 365 --quarantine ~/DigitalQuarantine --recursive
    ```

## 🧪 Testing

To ensure the Cosmic Dust Bunny Collector is ready for its mission, run the included tests:

1.  Navigate to the `utils/cosmic-dust-bunny-collector/` directory.
2.  Execute the tests using Python's `unittest` module:
    ```bash
    python -m unittest tests/test_collector.py
    ```

All tests are designed to be deterministic and do not interact with your actual filesystem, using mocks to simulate file operations and timestamps.

## 📜 License

This utility is released under the MIT License. See the main repository's `LICENSE` file for details.
