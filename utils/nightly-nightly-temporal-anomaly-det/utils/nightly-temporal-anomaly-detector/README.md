# Nightly Temporal Anomaly Detector

## 🌌 Unearthing Chronological Oddities in Your Filesystem 🌌

The Nightly Temporal Anomaly Detector is a whimsical yet practical utility designed to scan your project directories for files exhibiting unusual timestamp patterns. In the chaotic dance of development, files can sometimes acquire modification or creation dates that defy logic – existing in the future, or lingering from an epoch long past. This tool helps you pinpoint these chronological curiosities, aiding in repository hygiene, identifying forgotten assets, or debugging build system quirks.

### Features

*   **Future Modifiers**: Detects files whose last modification date is set in the future.
*   **Ancient Artifacts**: Identifies files that haven't been touched in a configurable long period (e.g., over a year).
*   **Pre-Genesis Creations**: Flags files with creation dates significantly older than a specified reference point, suggesting they might be misplaced or copied without proper timestamp resets.

### Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

```bash
# No installation needed, just run the script directly.
# Ensure you have Python 3.11+
python3 src/detector.py --help
```

### Usage

```bash
python3 src/detector.py <target_directory> [options]
```

**Arguments:**

*   `<target_directory>`: The path to the directory you wish to scan for temporal anomalies.

**Options:**

*   `--future-threshold <seconds>`: Files modified more than this many seconds in the future will be flagged. Default: `60` (1 minute).
*   `--stale-threshold <days>`: Files not modified in this many days will be flagged as ancient artifacts. Default: `365` (1 year).
*   `--creation-ref-date <YYYY-MM-DD>`: Files created before this date will be flagged as pre-genesis. Default: `2023-01-01` (a reasonable starting point for many projects).
*   `--exclude <pattern>`: A comma-separated list of glob patterns to exclude files or directories (e.g., `*.log,node_modules/*`).
*   `--verbose`: Print more detailed information about detected anomalies.

### Examples

Scan the current directory for anomalies:
```bash
python3 src/detector.py .
```

Scan a specific project directory, being stricter about future files and ignoring `node_modules`:
```bash
python3 src/detector.py /path/to/my/project --future-threshold 10 --exclude "node_modules/*"
```

Find files older than the project's inception date:
```bash
python3 src/detector.py . --creation-ref-date 2022-06-15
```

### How it Helps

*   **Repository Health**: Keep your codebase clean by identifying forgotten files or artifacts.
*   **Build System Debugging**: Future timestamps can break incremental builds or caching.
*   **Data Integrity**: Spot files that might have been incorrectly restored or copied.
*   **Historical Context**: Understand the true age and relevance of files in your project.

Embrace the temporal chaos, and bring order to your filesystem!
