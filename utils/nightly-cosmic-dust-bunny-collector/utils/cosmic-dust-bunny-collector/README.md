# Cosmic Dust Bunny Collector

## 🧹 Description

In the vast cosmos of your filesystem, forgotten files accumulate like cosmic dust bunnies, silently consuming precious space and digital energy. The `Cosmic Dust Bunny Collector` is your trusty broom, designed to whimsically yet effectively sweep away these digital relics.

This utility scans specified directories for files that haven't been modified or accessed in a configurable number of days. It can either list these 'dust bunnies' for your review (dry-run mode) or boldly remove them, freeing up space and bringing order to your digital universe.

## ✨ Features

*   **Targeted Sweeping**: Specify multiple directories to scan.
*   **Age-Based Filtering**: Only target files older than a defined threshold (e.g., 30 days).
*   **Dry-Run Mode**: Preview which files would be removed without actually deleting anything.
*   **Exclusion Patterns**: Ignore specific files or directories (e.g., `.git`, `node_modules`, `*.log`).
*   **Whimsical Output**: Enjoy a touch of cosmic charm with every cleanup.

## 🚀 Usage

### Prerequisites

*   Python 3.11+

### Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/cosmic-dust-bunny-collector/
```

### Running the Collector

```bash
python src/dust_bunny_collector.py --help
```

```
usage: dust_bunny_collector.py [-h] [--paths PATHS [PATHS ...]] [--age DAYS] [--dry-run] [--exclude EXCLUDE [EXCLUDE ...]]

Sweep away old, forgotten files ('cosmic dust bunnies') from specified directories.

options:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        Directories to scan for dust bunnies. Defaults to current directory.
  --age DAYS            Files older than this many days will be considered dust bunnies. Defaults to 30.
  --dry-run             Perform a dry run without actually deleting files.
  --exclude EXCLUDE [EXCLUDE ...]
                        File/directory patterns to exclude (e.g., '*.log', 'node_modules/').
```

**Example: Dry run in current directory for files older than 60 days**

```bash
python src/dust_bunny_collector.py --age 60 --dry-run
```

**Example: Clean up specific directories, excluding `.git` folders and `.tmp` files**

```bash
python src/dust_bunny_collector.py --paths /var/log /tmp/user_data --age 7 --exclude .git *.tmp
```

## 🧪 Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_dust_bunny_collector.py
```

## 📜 License

This utility is provided under the [MIT License](LICENSE).
