# Nightly Cache Purifier

## 🧹 Whimsical Purpose

In the post-apocalyptic digital wasteland, every byte of storage is a precious resource. The Nightly Cache Purifier is your trusty scavenger, designed to meticulously comb through the forgotten corners of your system, identifying and optionally purging the accumulated digital detritus of various applications and tools. Reclaim your disk space, and let your system breathe!

## ✨ Features

*   **Cross-Platform Cache Detection**: Identifies common user-level cache directories on Linux, macOS, and Windows.
*   **Dry Run Mode**: Safely preview which files and directories would be removed and how much space would be reclaimed without actually deleting anything.
*   **Interactive Cleaning**: Prompts for confirmation before performing any deletions.
*   **Space Reclamation Report**: Provides a summary of the space freed after a successful purge.

## 🚀 Usage

### Prerequisites

*   Python 3.8+

### Installation (Optional, for standalone use)

This utility is designed to be run directly. No special installation steps are required beyond having Python installed.

### Running the Purifier

Navigate to the `src` directory and run `purifier.py`:

```bash
python src/purifier.py --dry-run
```
This command will perform a dry run, listing all detected cache directories and the space they occupy, without deleting anything.

To actually clean the caches:

```bash
python src/purifier.py --clean
```
This will prompt you for confirmation before deleting files.

For a non-interactive clean (use with caution!):

```bash
python src/purifier.py --clean --force
```

### Command Line Arguments

*   `--dry-run`: (Default) Scan and report potential space savings without deleting anything.
*   `--clean`: Scan and prompt to delete detected caches.
*   `--force`: Use with `--clean` to skip confirmation prompts and delete immediately. **Use with extreme caution!**
*   `--verbose`: Show more detailed output during scanning.

## 🧪 Development & Testing

To run the tests, navigate to the `tests` directory and use `pytest`:

```bash
python -m pytest tests/
```

The tests use mocks to simulate file system operations, ensuring determinism and offline execution.
