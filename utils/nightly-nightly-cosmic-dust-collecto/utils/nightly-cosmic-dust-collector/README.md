# Nightly Cosmic Dust Collector

## 🌌 Overview

Welcome, digital custodians! The Nightly Cosmic Dust Collector is your trusty automated assistant for maintaining pristine digital environments. Just as cosmic dust accumulates in the vastness of space, digital detritus—old log files, temporary caches, and forgotten artifacts—can clutter your directories. This utility gracefully sweeps away files older than a specified age, ensuring your systems remain lean, efficient, and ready for whatever the apocalypse throws your way.

It's designed to be run as a nightly maintenance task, silently purging the digital dust bunnies that no longer serve a purpose.

## ✨ Features

*   **Age-based Deletion**: Removes files older than a configurable number of days.
*   **Directory Scan**: Targets specific directories for cleanup.
*   **Dry Run Mode**: Preview which files *would* be deleted without actually removing them.
*   **Logging**: Provides clear output on actions taken or proposed.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## 🚀 Usage

To run the Cosmic Dust Collector, execute the `dust_collector.py` script with the required arguments.

```bash
python src/dust_collector.py --directory <path/to/your/directory> --age <days> [--dry-run]
```

### Arguments:

*   `--directory <path>` (Required): The path to the directory you wish to clean.
*   `--age <days>` (Required): Files older than this many days will be considered 'cosmic dust' and targeted for removal.
*   `--dry-run` (Optional): If present, the utility will only report which files *would* be deleted without performing any actual deletions. Highly recommended for initial runs!

### Example:

To remove all files older than 30 days in `/var/log/my_app`:

```bash
python src/dust_collector.py --directory /var/log/my_app --age 30
```

To see what would be removed without actually deleting anything:

```bash
python src/dust_collector.py --directory /tmp/old_data --age 7 --dry-run
```

## 🛠️ Development

The utility is written in Python 3.11 and uses standard library modules. Tests are located in the `tests/` directory and can be run using `pytest` or `unittest`.

```bash
python -m unittest tests/test_dust_collector.py
```

Stay clean, stay efficient, and let the Cosmic Dust Collector handle the digital grime!
