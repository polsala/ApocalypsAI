# Apocalypse Artifact Archiver

This utility acts as a digital time capsule, preserving critical project artifacts for future civilizations (or just for quick reference). It takes a list of specified files and directories, copies them into a timestamped archive folder, ensuring that vital documentation and configurations are snapshotted.

## Usage

Run the `archiver.py` script with the `--output-dir` and `--files` arguments:

```bash
python src/archiver.py --output-dir ./archives --files README.md AGENTS.md LICENSE agents/
```

This will create a directory like `./archives/archive_YYYYMMDD_HHMMSS/` containing copies of `README.md`, `AGENTS.md`, `LICENSE`, and the entire `agents/` directory.

### Arguments

*   `--output-dir <path>`: The base directory where archives will be stored. (e.g., `./archives`)
*   `--files <file_or_dir> [<file_or_dir> ...]`: One or more paths to files or directories to be archived.

## Development

The archiver uses standard Python `shutil` and `datetime` modules. Tests are self-contained and use `unittest.mock` to simulate file system operations.
