# Nightly Data Debris Sweeper

## 🧹 Purpose

In the post-apocalyptic digital landscape, data debris accumulates like radioactive dust. The Nightly Data Debris Sweeper is your automated janitor, designed to meticulously identify and purge common temporary files, build artifacts, and cache directories that clutter your repository. Keep your wasteland (repository) clean, lean, and ready for the next build!

## ✨ Features

*   **Configurable Patterns**: Define custom file and directory patterns to target for sweeping.
*   **Dry Run Mode**: Preview what will be swept away before any permanent deletion.
*   **Recursive Cleaning**: Scans subdirectories to ensure no debris is left unturned.
*   **Whimsical Output**: Provides a clear, slightly dramatic summary of the cleaning operation.

## 🚀 Usage

```bash
python src/sweeper.py [path] [--dry-run] [--patterns <pattern1> <pattern2> ...]
```

### Arguments:

*   `path`: (Optional) The root directory to start sweeping from. Defaults to the current working directory (`.`).
*   `--dry-run`: (Optional) If present, the utility will only report what *would* be deleted without actually deleting anything.
*   `--patterns`: (Optional) A space-separated list of glob patterns (e.g., `*.log`, `__pycache__`, `node_modules/`). Overrides default patterns.

### Examples:

1.  **Clean current directory with default patterns (dry run):**
    ```bash
    python src/sweeper.py --dry-run
    ```

2.  **Clean a specific directory, deleting files:**
    ```bash
    python src/sweeper.py /path/to/my/project
    ```

3.  **Clean with custom patterns:**
    ```bash
    python src/sweeper.py --patterns "*.tmp" "build/" "dist/"
    ```

## ⚙️ Default Patterns

By default, the sweeper targets the following common debris:

*   `__pycache__`
*   `.pytest_cache`
*   `.mypy_cache`
*   `.DS_Store`
*   `*.log`
*   `*.tmp`
*   `node_modules/`
*   `target/` (common for Rust/Java builds)
*   `dist/`
*   `build/`
*   `.coverage`
*   `.venv/` (be careful with this one, it's often useful!)

## ⚠️ Warning

Use with caution! While the dry-run mode is helpful, ensure you understand what patterns you are applying before permanent deletion. The ApocalypsAI is not responsible for accidentally swept-away survival rations (important files).

## 🧪 Development & Testing

To run tests:

```bash
python -m unittest tests/test_sweeper.py
```
