# Apocalypse Cache Cleaner

In these trying times, digital scarcity is a real threat. The Apocalypse Cache Cleaner helps you conserve precious disk space, ensuring your projects remain lean and mean for the inevitable.

## Purpose

This utility scans a specified directory for common project cache and build folders (e.g., `__pycache__`, `node_modules`, `.venv`, `target`, `dist`, `build`). It reports their total size and, optionally, allows you to delete them to free up disk space.

## Usage

Run the script from your terminal:

```bash
python src/cache_cleaner.py <path_to_scan> [--delete]
```

- `<path_to_scan>`: The root directory to start scanning from (e.g., `.` for the current directory).
- `--delete`: (Optional) If present, the utility will prompt you to confirm deletion of the identified cache directories. Without this flag, it will only report.

### Examples

Scan the current directory and report:

```bash
python src/cache_cleaner.py .
```

Scan a specific project directory and delete caches after confirmation:

```bash
python src/cache_cleaner.py ~/my_project --delete
```

## Supported Cache Patterns

The utility looks for directories matching these patterns (case-insensitive):

- `__pycache__` (Python)
- `.pytest_cache` (Python)
- `.mypy_cache` (Python)
- `.venv` (Python virtual environments)
- `venv` (Python virtual environments)
- `node_modules` (Node.js/npm)
- `dist` (Build output)
- `build` (Build output)
- `target` (Rust/Maven build output)
- `out` (General output)
- `tmp` (Temporary files)
