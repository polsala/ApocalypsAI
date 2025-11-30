# Nightly Cosmic Cache Cleaner

## 🌌 Purify Your Digital Nebula! 🌌

The Nightly Cosmic Cache Cleaner is a whimsical yet powerful Python utility designed to help you maintain a pristine development environment by eradicating temporary files, cache directories, and build artifacts that accumulate over time. Think of it as a digital black hole, gracefully absorbing the cosmic clutter from your project directories.

### ✨ Features

*   **Configurable Cleansing**: Define specific file patterns and directory names to target for removal.
*   **Dry Run Mode**: Preview what will be removed before committing to the cleanse, ensuring no essential cosmic dust is disturbed.
*   **Whimsical Output**: Enjoy space-themed messages as your workspace is purified.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

### 🚀 Usage

1.  **Navigate to your project directory**:
    ```bash
    cd /path/to/your/project
    ```

2.  **Run the cleaner in dry-run mode (recommended first!)**:
    This will show you what files and directories *would* be removed without actually deleting anything.
    ```bash
    python3 /path/to/ApocalypsAI/utils/nightly-cosmic-cache-cleaner/src/cleaner.py --path . --dry-run
    ```

3.  **Perform the actual cleansing**:
    If you're satisfied with the dry-run output, remove the `--dry-run` flag to initiate the cosmic purification.
    ```bash
    python3 /path/to/ApocalypsAI/utils/nightly-cosmic-cache-cleaner/src/cleaner.py --path .
    ```

    You can also specify a different path to clean:
    ```bash
    python3 /path/to/ApocalypsAI/utils/nightly-cosmic-cache-cleaner/src/cleaner.py --path /another/project/directory
    ```

### ⚙️ Configuration

The cleaner uses a default set of patterns and directories to target. You can customize this by modifying the `DEFAULT_CLEAN_CONFIG` dictionary within `src/cleaner.py`.

**Default Configuration Targets:**

*   `__pycache__` directories
*   `.pytest_cache` directories
*   `build/` directories
*   `dist/` directories
*   `.mypy_cache` directories
*   `.venv` (Python virtual environments)
*   `env` (Another common virtual environment name)
*   `*.pyc` files
*   `*.log` files
*   `.DS_Store` files (macOS)
*   `Thumbs.db` files (Windows)
*   `*.bak` files
*   `*.tmp` files

### ⚠️ Warning

Always use the `--dry-run` option first to review the proposed changes. While this utility is designed to target common temporary files, incorrect configuration or usage could lead to unintended data loss, especially when including virtual environment directories like `.venv` or `env`. Use with cosmic caution!
