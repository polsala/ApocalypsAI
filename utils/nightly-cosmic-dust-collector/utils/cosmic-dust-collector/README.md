# Cosmic Dust Collector

## Purpose
This utility, the 'Cosmic Dust Collector,' is designed to help maintain a pristine repository by identifying and optionally removing old, temporary, or otherwise specified 'dust' files and directories. Think of it as a digital broom for your project directories, sweeping away the accumulated cruft of development.

## Usage
Run the `dust_collector.py` script with the desired path and options.

```bash
python src/dust_collector.py --path <directory_to_scan> \
                              [--age <days>] \
                              [--patterns <glob_pattern_1> <glob_pattern_2> ...] \
                              [--delete]
```

## Options
*   `--path <directory>` (Required): The root directory to start scanning for dust.
*   `--age <days>` (Optional): Only consider files older than this many days. Default is 30 days.
*   `--patterns <glob_pattern_1> ...` (Optional): One or more glob patterns (e.g., `*.log`, `temp_*`, `__pycache__`, `.DS_Store`) to match against filenames or directory names. If not provided, all files older than `--age` are considered.
*   `--delete` (Optional): If present, the utility will actually delete the identified dust files. **Use with caution!** By default, it performs a dry run and only reports.

## Examples

### Report all files older than 60 days in the current directory:
```bash
python src/dust_collector.py --path . --age 60
```

### Delete all `.log` and `.tmp` files older than 7 days in a specific project folder:
```bash
python src/dust_collector.py --path /path/to/my/project --age 7 --patterns "*.log" "*.tmp" --delete
```

### Find all `__pycache__` directories and `.DS_Store` files, regardless of age (dry run):
```bash
python src/dust_collector.py --path . --patterns "__pycache__" ".DS_Store"
```
