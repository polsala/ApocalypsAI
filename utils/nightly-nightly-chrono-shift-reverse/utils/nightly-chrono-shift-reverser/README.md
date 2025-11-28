# Nightly Chrono-Shift Reverser

## Overview
The Nightly Chrono-Shift Reverser is a whimsical yet practical utility designed to manage temporary or old files in a safe and reversible manner. Instead of permanently deleting files that exceed a certain age, it 'chrono-shifts' them into a timestamped quarantine directory. This provides a safety net, allowing you to easily inspect and restore files if they were moved by mistake.

## How it Works
1.  **Scan**: The utility scans a specified target directory for files.
2.  **Identify Old Files**: It identifies files older than a configured age threshold (e.g., 7 days).
3.  **Quarantine**: Instead of deleting, these old files are moved into a special `.quarantine/` subdirectory within the target directory. Each cleanup operation creates a new timestamped subfolder (e.g., `.quarantine/2023-10-27_14-30-00/`) to store the moved files, preserving the original directory structure within that batch.
4.  **Restore (Optional)**: You can list all quarantined batches and, if needed, restore an entire batch of files back to their original location in the target directory.

## Usage

### Prerequisites
*   Python 3.6+

### Running the Cleaner
To clean files older than 7 days in the current directory:

```bash
python src/reverser.py clean . --age 7
```

To clean files in a specific directory (e.g., `/var/log/temp`) older than 30 days:

```bash
python src/reverser.py clean /var/log/temp --age 30
```

### Listing Quarantined Batches
To see what batches of files have been quarantined in the current directory:

```bash
python src/reverser.py list .
```

### Restoring a Quarantined Batch
First, list the batches to find the `BATCH_NAME` (e.g., `2023-10-27_14-30-00`). Then, to restore:

```bash
python src/reverser.py restore . --batch 2023-10-27_14-30-00
```

**Note**: Restoring a batch will move all files from that batch back to the top-level target directory. If files with the same name already exist, they will be overwritten. Use with caution.

## Development

### Running Tests
```bash
python -m unittest tests/test_reverser.py
```
