# Nightly Cosmic Dust Collector

## Description

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help maintain a tidy filesystem. It scans specified directories for files that match certain patterns and are older than a configured age, then removes them. Think of it as a diligent space janitor, sweeping away the digital detritus that accumulates over time.

This tool is perfect for cleaning up temporary files, old log archives, build artifacts, or any other 'cosmic dust' that clutters your development or system directories.

## Usage

Run the utility from the command line:

```bash
python src/dust_collector.py --path /path/to/clean --config config.yaml [--dry-run]
```

### Arguments:

*   `--path <directory>`: The root directory to start cleaning from. This argument is required.
*   `--config <file.yaml>`: Path to a YAML configuration file. This argument is required.
*   `--dry-run`: If present, the utility will only report which files *would* be removed, without actually deleting them. Highly recommended for initial runs.

## Configuration (config.yaml)

The configuration file is a YAML file that defines the rules for dust collection. It must contain a list of `rules`, where each rule specifies `patterns` and a `max_age_days`.

### Example `config.yaml`:

```yaml
rules:
  - name: "Temporary Files"
    patterns:
      - "*.tmp"
      - "*.temp"
      - "temp_*"
    max_age_days: 7
  - name: "Old Log Archives"
    patterns:
      - "*.log.gz"
      - "*.log.zip"
    max_age_days: 30
  - name: "Build Artifacts"
    patterns:
      - "dist/*"
      - "build/*"
      - "__pycache__/*"
    max_age_days: 14
```

*   `name`: (Optional) A descriptive name for the rule.
*   `patterns`: A list of glob-style patterns (e.g., `*.log`, `temp_*`, `dist/*`). Files matching any of these patterns will be considered.
*   `max_age_days`: The maximum age in days for a file. Files older than this age will be targeted for removal.

## Installation

This utility is self-contained and written in Python 3.11. It requires `PyYAML` for configuration parsing. You can install it using pip:

```bash
pip install PyYAML
```

Then, simply place `src/dust_collector.py` and your `config.yaml` in your desired location and run it.
