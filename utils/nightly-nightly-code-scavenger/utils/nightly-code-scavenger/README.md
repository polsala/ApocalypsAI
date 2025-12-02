# Nightly Code Scavenger

The digital wasteland can accumulate a lot of forgotten debris. The Nightly Code Scavenger is here to help you unearth those hidden relics – empty directories, ancient files, and temporary detritus – that might be cluttering your precious repository. Keep your digital bunker tidy and efficient!

## Purpose

This utility scans a specified directory for:
1.  **Empty directories**: Directories containing no files or subdirectories.
2.  **Old files**: Files not modified within a configurable timeframe (default: 365 days).
3.  **Temporary/Log files**: Files matching common patterns for temporary or log data (e.g., `*.log`, `*.tmp`, `__pycache__` directories).

It generates a report, helping you decide what to clean up, ensuring your repository remains lean and mean for the coming apocalypse.

## Usage

```bash
python src/scavenger.py <path_to_scan> [--max-age-days <days>] [--exclude <pattern>]
```

### Arguments:
*   `<path_to_scan>`: The root directory to begin scavenging.
*   `--max-age-days <days>`: (Optional) Files older than this many days will be flagged as 'old'. Default is 365 days.
*   `--exclude <pattern>`: (Optional, can be repeated) A glob pattern to exclude files or directories from scanning (e.g., `*.git*`, `node_modules`).

### Example:
```bash
python src/scavenger.py . --max-age-days 180 --exclude "*/.git/*" --exclude "*/node_modules/*"
```

## Output

The scavenger will print a report to standard output, categorizing the findings:

```
Scavenging report for: /path/to/your/repo

--- Empty Directories ---
- /path/to/your/repo/empty_folder_1
- /path/to/your/repo/another/empty_folder_2

--- Old Files (modified > 365 days ago) ---
- /path/to/your/repo/old_script.py (Last modified: YYYY-MM-DD)
- /path/to/your/repo/docs/ancient_notes.txt (Last modified: YYYY-MM-DD)

--- Temporary/Log Files ---
- /path/to/your/repo/temp/cache.tmp
- /path/to/your/repo/logs/app.log
- /path/to/your/repo/__pycache__/
```

## Development

To run tests:
```bash
python -m unittest tests/test_scavenger.py
```
