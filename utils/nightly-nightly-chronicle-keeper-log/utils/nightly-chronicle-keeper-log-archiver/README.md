# Nightly Chronicle Keeper Log Archiver

## 📜 Overview

The Nightly Chronicle Keeper Log Archiver is a whimsical-yet-useful utility designed to help you maintain a tidy digital history of your daily activities, system logs, or any ephemeral text files. In the post-apocalyptic landscape of digital clutter, this tool ensures your valuable chronicles are neatly bundled and preserved, preventing information overload while keeping a record of the past.

It scans a specified source directory for log files, consolidates their content into a single, timestamped archive file, and optionally cleans up the originals. Perfect for archiving daily agent run logs, system reports, or your personal survival journal entries.

## ✨ Features

*   **Consolidate**: Merges content from multiple log files into one.
*   **Timestamped Archives**: Creates uniquely named archive files for easy chronological tracking.
*   **Cleanup**: Optionally removes original log files after successful archiving.
*   **Self-contained**: No external dependencies beyond Python's standard library.

## 🚀 Usage

```bash
python src/archiver.py --source <source_directory> --archive <archive_directory> [--delete-originals]
```

### Arguments:

*   `--source <source_directory>`: The directory containing the log files to be archived.
*   `--archive <archive_directory>`: The directory where the consolidated archive file will be saved.
*   `--delete-originals`: (Optional) If provided, the original log files in the source directory will be deleted after successful archiving.

### Example:

```bash
# Archive logs from 'my_agent_logs' into 'archive_vault', keeping originals
python src/archiver.py --source my_agent_logs --archive archive_vault

# Archive logs and delete originals
python src/archiver.py --source daily_reports --archive historical_data --delete-originals
```

## 🛠️ Development

The utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

To ensure the Chronicle Keeper is in top shape, run its self-contained tests:

```bash
python -m unittest tests/test_archiver.py
```
