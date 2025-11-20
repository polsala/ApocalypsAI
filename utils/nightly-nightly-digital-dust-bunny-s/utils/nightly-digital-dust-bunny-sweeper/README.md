# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

In the post-apocalyptic digital landscape, every byte counts! The "Nightly Digital Dust Bunny Sweeper" is a whimsical yet essential utility designed to help you reclaim precious disk space by identifying and optionally removing old, unused, or temporary files that accumulate like digital dust bunnies. Keep your systems lean, mean, and ready for whatever the wasteland throws at them.

## ✨ Features

*   **Pattern-Based Scanning**: Define file name patterns (e.g., `*.tmp`, `*.log.old`, `~*`) to target specific types of digital clutter.
*   **Age-Based Filtering**: Only target files older than a specified number of days, ensuring you don't accidentally sweep away recent work.
*   **Dry Run Mode**: Preview which files *would* be deleted without actually removing them, for peace of mind.
*   **Interactive Confirmation**: For actual deletion, prompt for confirmation before proceeding.
*   **Recursive Scanning**: Traverse directories to find dust bunnies hiding deep within your file system.

## 🚀 Usage

### Installation (No installation needed, just run the script!)

1.  Navigate to the `src` directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-sweeper/src
    ```

### Running the Sweeper

The `sweeper.py` script can be run directly from your terminal.

```bash
python sweeper.py --help
```

```
usage: sweeper.py [-h] [-d DIRECTORY] [-p PATTERN] [-a AGE_DAYS] [--dry-run] [--force]

Clean up old, unused, or temporary files.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to scan (default: current directory)
  -p PATTERN, --pattern PATTERN
                        File pattern to match (e.g., '*.tmp', 'backup_*', can be repeated)
  -a AGE_DAYS, --age-days AGE_DAYS
                        Delete files older than this many days (default: 30)
  --dry-run             Simulate deletion without actually removing files.
  --force               Skip interactive confirmation for deletion.
```

**Examples:**

1.  **Dry run to find all `.tmp` files older than 7 days in the current directory:**
    ```bash
    python sweeper.py --pattern "*.tmp" --age-days 7 --dry-run
    ```

2.  **Delete `.log.old` and files starting with `~` older than 30 days in `/var/log/old_logs` (with confirmation):**
    ```bash
    python sweeper.py --directory /var/log/old_logs --pattern "*.log.old" --pattern "~*" --age-days 30
    ```

3.  **Force delete all files ending with `~` older than 1 day in your home directory, without confirmation:**
    ```bash
    python sweeper.py --directory ~/ --pattern "*~" --age-days 1 --force
    ```

## 🧪 Development & Testing

To run the tests, navigate to the `tests` directory and execute `pytest` (or `python -m unittest` if `pytest` is not available globally).

```bash
cd utils/nightly-digital-dust-bunny-sweeper/tests
python -m unittest test_sweeper.py
```

## 📜 License

This utility is released under the MIT License. See the `LICENSE` file in the repository root for more details.
