# Nightly Cosmic Dust Bunny Collector

## 🌌🧹 Description

The universe is vast, and so is your hard drive! Over time, temporary files, old logs, and forgotten caches accumulate like cosmic dust bunnies, silently consuming precious space and slowing down your system. The **Nightly Cosmic Dust Bunny Collector** is here to help!

This whimsical-yet-useful utility scans specified directories for files matching configurable patterns and age thresholds, allowing you to identify and optionally purge these digital detritus. Keep your system sparkling clean and ready for the next apocalypse (or just your next coding session).

## ✨ Features

*   **Pattern-based Scanning**: Define file extensions or name patterns (e.g., `*.log`, `*.tmp`, `~*`) to target specific types of "dust bunnies."
*   **Age-based Filtering**: Only target files older than a specified number of days, ensuring you don't accidentally sweep away recent work.
*   **Dry Run Mode**: Safely preview which files would be collected without actually deleting anything.
*   **Configurable Directories**: Specify multiple paths to scan, from your project folders to system-wide temporary directories.
*   **Self-contained & Portable**: Written in Python, easy to run anywhere.

## 🚀 Usage

```bash
python src/collector.py --help
```

### Basic Scan (Dry Run)

To see what cosmic dust bunnies are lurking in your `~/my_project` directory, looking for `.log` and `.tmp` files older than 7 days:

```bash
python src/collector.py \
    --path ~/my_project \
    --patterns "*.log" "*.tmp" \
    --age 7 \
    --dry-run
```

### Deleting Dust Bunnies

Once you're confident with the dry run output, you can proceed with deletion:

```bash
python src/collector.py \
    --path ~/my_project \
    --patterns "*.log" "*.tmp" \
    --age 7 \
    --delete
```

### Scanning Multiple Paths

```bash
python src/collector.py \
    --path /var/log \
    --path /tmp \
    --patterns "*.old" "*.bak" \
    --age 30 \
    --dry-run
```

## 🛠️ Development

### Requirements

*   Python 3.8+

### Running Tests

```bash
python -m unittest tests/test_collector.py
```
