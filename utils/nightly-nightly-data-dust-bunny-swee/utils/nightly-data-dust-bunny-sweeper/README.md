# Nightly Data Dust-Bunny Sweeper

The ApocalypsAI Nightly Data Dust-Bunny Sweeper is a whimsical-yet-useful utility designed to help keep your project directories tidy and free from digital clutter. It scans specified paths for old, unused, or temporary files (our beloved "dust bunnies") based on their age and file patterns, providing a report or optionally cleaning them up.

## Features

*   **Age-based detection**: Identify files older than a configurable number of days.
*   **Pattern matching**: Target specific file types like temporary files (`.tmp`), log files (`.log`), backup files (`.bak`), or editor swap files (`~*`).
*   **Dry run mode**: Safely preview which files would be affected before any deletion.
*   **Optional cleanup**: Delete identified "dust bunnies" to reclaim disk space and reduce repository bloat.

## Usage

```bash
python src/sweeper.py --path /path/to/scan --age-days 90 --patterns "*.tmp,*.log,*.bak"
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. Defaults to the current working directory.
*   `--age-days <int>`: Files older than this many days will be considered "dust bunnies". Defaults to 30 days.
*   `--patterns <glob1,glob2,...>`: A comma-separated list of glob patterns to match against filenames. Defaults to `*.tmp,*.log,*.bak,~*`.
*   `--clean`: If present, identified files will be deleted. Use with caution!
*   `--dry-run`: If present, the utility will only report files and will not delete anything, even if `--clean` is specified. This is the default behavior if `--clean` is not provided.

## Examples

Scan the current directory for files older than 60 days matching `.log` or `.old` patterns, and report them:
```bash
python src/sweeper.py --age-days 60 --patterns "*.log,*.old"
```

Scan a specific project directory for default patterns, older than 7 days, and actually delete them:
```bash
python src/sweeper.py --path /home/user/my_project --age-days 7 --clean
```

Perform a dry run for files older than 180 days matching any pattern:
```bash
python src/sweeper.py --path /var/log --age-days 180 --patterns "*" --dry-run
```

## Development

### Running Tests

```bash
python -m unittest tests/test_sweeper.py
```
