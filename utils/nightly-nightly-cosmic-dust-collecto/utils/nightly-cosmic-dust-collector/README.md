# Nightly Cosmic Dust Collector

Ever feel like your repository is accumulating tiny, forgotten files, like cosmic dust motes settling on the digital landscape? This utility is your nightly janitor, designed to sweep through your specified directories, identify these minuscule digital specks, and help you decide their fate.

It's perfect for tidying up build artifacts, old logs, empty placeholder files, or any other digital detritus that might be silently taking up space.

## Usage

```bash
python src/dust_collector.py <path_to_scan> [--threshold <bytes>] [--quarantine]
```

- `<path_to_scan>`: The root directory to begin the cosmic dust sweep.
- `--threshold <bytes>`: (Optional) The maximum file size (in bytes) to consider as 'cosmic dust'. Files larger than this will be ignored. Defaults to `1024` bytes (1KB).
- `--quarantine`: (Optional) If provided, identified 'dust' files will be moved to a `.quarantine` subdirectory within their original parent directory, rather than just being reported. This allows for later review or deletion.

## Examples

Scan the current directory for files smaller than 500 bytes and report them:
```bash
python src/dust_collector.py . --threshold 500
```

Scan a 'build' directory for files smaller than 1KB and move them to quarantine:
```bash
python src/dust_collector.py ./build --quarantine
```

## Installation

This utility is self-contained and requires no external dependencies beyond standard Python 3.11 libraries. Simply place it in your `utils/` directory and run.
