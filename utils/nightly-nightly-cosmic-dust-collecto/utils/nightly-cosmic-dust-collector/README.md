# Nightly Cosmic Dust Collector

## 🌌 Purpose

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help keep your digital workspace tidy. It scans specified directories for "cosmic dust" – forgotten, old, or temporary files that accumulate over time, cluttering your project and consuming precious disk space. Think of it as a digital broom for the forgotten corners of your repository.

## ✨ Features

*   **Identify Dust**: Locates empty files, files older than a configurable age, and files matching specific patterns (e.g., `.tmp`, `.bak`).
*   **Dry Run Mode**: Safely preview which files would be affected without making any changes.
*   **Collect to Dustbin**: Move identified "dust" files to a designated "cosmic dustbin" directory for later review or disposal.
*   **Configurable**: Adjust age thresholds and file patterns to suit your needs.

## 🚀 Usage

The utility is a Python script that can be run from the command line.

```bash
python src/dust_collector.py --help
```

### Basic Scan (Dry Run)

To simply list the "cosmic dust" in your current directory and its subdirectories without making any changes:

```bash
python src/dust_collector.py --root-dir .
```

### Scan and Move to Dustbin

To move identified dust files to a `_cosmic_dustbin` directory (it will be created if it doesn't exist):

```bash
python src/dust_collector.py --root-dir /path/to/your/project --dustbin-dir /path/to/your/project/_cosmic_dustbin --no-dry-run
```

### Customizing Dust Collection

*   **Age Threshold**: Find files older than 180 days:
    ```bash
    python src/dust_collector.py --root-dir . --age-threshold-days 180
    ```
*   **Specific Patterns**: Find `.tmp` and `.log` files:
    ```bash
    python src/dust_collector.py --root-dir . --patterns "*.tmp" "*.log"
    ```
    (Note: patterns use `fnmatch` style, not regex.)

## 🛠️ Development

### Requirements

*   Python 3.8+ (tested with 3.11)

### Running Tests

Navigate to the `utils/nightly-cosmic-dust-collector` directory and run:

```bash
python -m unittest tests/test_dust_collector.py
```
