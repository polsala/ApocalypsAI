# Nightly Digital Debris Sweeper

## 🧹 Purpose

The ApocalypsAI Nightly Digital Debris Sweeper is a whimsical-yet-useful utility designed to help you maintain a clean and organized digital workspace. As the end times approach (or just another Tuesday), temporary files, old logs, and forgotten backups can accumulate, cluttering your directories and consuming precious disk space. This utility acts as your vigilant digital janitor, identifying and optionally quarantining these "debris" files.

Think of it as a pre-apocalyptic spring cleaning for your file system!

## ✨ Features

*   **Pattern-Based Scanning**: Define custom file patterns (e.g., `*.log`, `*.tmp`, `*~`) to identify unwanted files.
*   **Age Filtering**: Optionally only target files older than a specified number of days, ensuring you don't sweep away recently created (and potentially still useful) temporary files.
*   **Multiple Scan Directories**: Scan one or more directories simultaneously.
*   **List-Only Mode**: Preview what files would be affected before committing to any changes.
*   **Quarantine Functionality**: Move identified debris files to a designated "quarantine" directory, rather than deleting them, providing a safety net for accidental sweeps.
*   **Collision Handling**: Automatically renames files if a name collision occurs in the quarantine directory (e.g., `error.log` becomes `error_1.log`).

## 🚀 Usage

The utility is a Python 3.11 script and can be run directly.

```bash
python src/sweeper.py --help
```

### Basic Scan (List Only)

To simply list all identified debris files in a directory without moving them:

```bash
python src/sweeper.py /path/to/your/project /path/to/another/folder --patterns "*.log" "*.tmp"
```

### Quarantining Debris

To move identified debris files to a quarantine directory:

```bash
python src/sweeper.py /path/to/scan --quarantine-dir /path/to/quarantine/folder
```

**Note**: If the `--quarantine-dir` is not specified, the utility will only list files. If `--list-only` is used, it will override `--quarantine-dir` and only list files.

### Advanced Usage with Age Filter

To quarantine only `.log` files older than 30 days in your home directory:

```bash
python src/sweeper.py ~/my_app_logs --patterns "*.log" --age-days 30 --quarantine-dir ~/debris_quarantine
```

### Command-Line Arguments

*   `scan_dirs` (positional, required): One or more directories to scan for debris.
*   `--patterns` (optional, default: `*.log *.tmp *~ *.bak *.old`): Space-separated list of file patterns to identify as debris.
*   `--quarantine-dir` (optional): Directory to move identified debris files to. If not specified, files will only be listed.
*   `--age-days` (optional, default: `0`): Only consider files older than this many days as debris. Set to `0` to ignore age.
*   `--list-only` (optional, flag): Only list debris files, do not move them. Overrides `--quarantine-dir` if present.

## 🧪 Testing

To run the tests for this utility, navigate to the `utils/nightly-digital-debris-sweeper` directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```

The tests are designed to be deterministic and offline, using Python's `unittest.mock` to simulate file system operations without actually touching your disk.
