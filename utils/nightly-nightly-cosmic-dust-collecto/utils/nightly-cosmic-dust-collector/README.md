# Nightly Cosmic Dust Collector

## Description

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a clean and organized repository. It scans a specified directory for files that haven't been modified for a certain period, identifying them as 'cosmic dust' that might be cluttering your digital space. This helps in proactively managing old logs, temporary build artifacts, or forgotten files.

## Usage

Run the utility from the command line, providing the path to scan and an optional age threshold.

```bash
python src/dust_collector.py <path_to_scan> [--age-days <int>] [--exclude <pattern>] [--output-format <text|json>]
```

### Arguments:

*   `<path_to_scan>`: The root directory to begin scanning for dusty files.
*   `--age-days <int>`: (Optional) The minimum age in days for a file to be considered 'dusty'. Defaults to 90 days.
*   `--exclude <pattern>`: (Optional, can be repeated) A glob-style pattern (e.g., `*.log`, `temp/*`) to exclude files or directories from the scan. Exclusions are applied to the full path.
*   `--output-format <text|json>`: (Optional) Specify the output format. Defaults to `text`. Use `json` for machine-readable output.

### Examples:

Scan the current directory for files older than 60 days, excluding `.git` and `node_modules` directories:

```bash
python src/dust_collector.py . --age-days 60 --exclude '.git/*' --exclude 'node_modules/*'
```

Scan a specific log directory and output results as JSON:

```bash
python src/dust_collector.py /var/log/app --age-days 30 --exclude '*.gz' --output-format json
```

## Output (text format)

```
Cosmic Dust Report for: /path/to/repo (older than 90 days)
-----------------------------------------------------------
Found 3 dusty files:
  - /path/to/repo/old_log.txt (Last modified: 2023-01-15)
  - /path/to/repo/temp/build_artifact.tmp (Last modified: 2023-02-01)
  - /path/to/repo/docs/draft.md (Last modified: 2023-03-10)
```

## Output (json format)

```json
{
  "scan_path": "/path/to/repo",
  "age_threshold_days": 90,
  "scan_date": "2024-04-23T10:00:00Z",
  "dusty_files": [
    {
      "path": "/path/to/repo/old_log.txt",
      "last_modified": "2023-01-15T12:30:00Z"
    },
    {
      "path": "/path/to/repo/temp/build_artifact.tmp",
      "last_modified": "2023-02-01T08:00:00Z"
    },
    {
      "path": "/path/to/repo/docs/draft.md",
      "last_modified": "2023-03-10T16:45:00Z"
    }
  ]
}
```
