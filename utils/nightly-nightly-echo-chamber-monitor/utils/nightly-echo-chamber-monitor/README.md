# Nightly Echo Chamber Monitor

## 🌌 Silence the Echoes, Reclaim the Void 🌌

The Nightly Echo Chamber Monitor is a whimsical yet powerful utility designed to detect and report duplicate files within your specified directories. In the vast digital expanse, redundant files can create "echoes" that consume precious storage space. This monitor helps you identify these echoes, allowing you to silence them and reclaim the void for more vital data.

### Features

*   **Duplicate Detection**: Scans directories and their subdirectories to find files with identical content (based on SHA256 hash).
*   **Configurable Paths**: Specify one or more directories to scan.
*   **Report Generation**: Outputs a clear list of duplicate file groups, showing all paths for each identical file.
*   **Lightweight & Self-contained**: Written in Python, with minimal dependencies, making it easy to run anywhere.

### Usage

```bash
python src/echo_chamber_monitor.py --path /path/to/scan1 --path /path/to/scan2
```

#### Arguments

*   `--path <directory>`: One or more paths to directories to scan for duplicates. This argument can be provided multiple times. (Required)
*   `--min-size <bytes>`: Minimum file size (in bytes) to consider for hashing. Files smaller than this will be ignored. Defaults to 1 byte (i.e., ignores empty files).
*   `--output <file>`: Optional. Path to a file where the report will be written. If not provided, the report is printed to stdout.

### Example Output

```
--- Duplicate Files Found ---

Group 1 (SHA256: a1b2c3d4e5f6...)
  - /home/user/documents/report_v1.pdf
  - /home/user/backups/report_v1_copy.pdf

Group 2 (SHA256: f6e5d4c3b2a1...)
  - /var/log/app/debug.log.old
  - /tmp/debug.log.backup
  - /home/user/archive/old_logs/debug.log

--- End of Report ---
```

### Installation

This utility is self-contained. Simply clone the `ApocalypsAI` repository and navigate to `utils/nightly-echo-chamber-monitor`.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-echo-chamber-monitor
python src/echo_chamber_monitor.py --help
```

### Contributing

Feel free to contribute to the Echo Chamber Monitor by opening issues or pull requests in the main ApocalypsAI repository.
