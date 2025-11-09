# Nightly Gravitational Pull Optimizer

## Overview

The `nightly-gravitational-pull-optimizer` is a whimsical-yet-useful utility designed to help maintain a lean and efficient repository. It scans your project directory for large files and directories, identifying those that contribute significantly to the repository's 'gravitational pull' (i.e., its size). By highlighting these 'heavy' components, it provides actionable insights for optimization, such as considering Git LFS for large binaries, cleaning up build artifacts, or refactoring large data files.

## How it Works

The utility recursively traverses the specified directory (defaults to the current working directory), calculates the size of each file, and aggregates total sizes for directories (including their contents). It then reports files and directories exceeding a configurable size threshold, sorted by their contribution to the total size.

## Usage

To run the optimizer, navigate to your repository's root or any desired subdirectory and execute the `optimizer.py` script.

```bash
python src/optimizer.py [path] [--threshold <size_in_MB>]
```

- `path`: (Optional) The directory to scan. Defaults to the current working directory (`.`).
- `--threshold <size_in_MB>`: (Optional) The minimum size (in Megabytes) for a file or directory to be reported. Defaults to `10` MB.

### Examples:

Scan the current directory with the default threshold (10MB):
```bash
python src/optimizer.py
```

Scan a specific 'assets' directory with a 50MB threshold:
```bash
python src/optimizer.py assets --threshold 50
```

## Output Example

```
Scanning directory: .

Heavy Components (Threshold: 10.00 MB):
----------------------------------------
[DIR] 155.00 MB: /mock_repo/build
[DIR] 75.20 MB: /mock_repo/data
[FILE] 75.00 MB: /mock_repo/data/huge_dataset.csv
----------------------------------------
Total heavy components found: 3
```
