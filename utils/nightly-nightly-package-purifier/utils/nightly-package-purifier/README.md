# ApocalypsAI Nightly Package Purifier

## 🧹 Post-Apocalyptic Package Purifier 🧹

In the desolate landscape of your project directories, digital debris accumulates. `nightly-package-purifier` is your trusty companion, designed to scavenge and purge the forgotten caches, build artifacts, and temporary files that bloat your disk space and clutter your workspace. Keep your projects lean, mean, and ready for the next build cycle!

### ✨ Features

*   **Multi-Ecosystem Support**: Identifies common artifacts from Python, Node.js, Rust, Go, Java (Maven/Gradle), and more.
*   **Dry Run Mode**: Safely preview what would be removed before committing to the purge.
*   **Configurable Patterns**: Extend or override the default cleanup patterns to suit your specific needs.
*   **Disk Space Reporting**: Shows you how much precious disk space you'll reclaim.

### 🚀 Usage

Navigate to your project's root directory or specify a target path.

```bash
# List all identified artifacts without deleting them (recommended first step)
python src/purifier.py --list

# List artifacts in a specific directory
python src/purifier.py /path/to/your/project --list

# Actually clean up the identified artifacts (use with caution!)
python src/purifier.py --clean

# Clean up artifacts in a specific directory
python src/purifier.py /path/to/your/project --clean

# Use custom patterns (overrides defaults) - e.g., only clean 'temp_dir' and 'log_files'
python src/purifier.py --patterns temp_dir log_files --clean

# Use custom patterns with a specific path
python src/purifier.py /path/to/another/project --patterns custom_cache --list
```

### 🗑️ Default Cleanup Patterns

The purifier targets the following common directories and files by default:

*   `__pycache__` (Python bytecode cache)
*   `.pytest_cache` (pytest cache)
*   `.venv` (Python virtual environment)
*   `venv` (Python virtual environment)
*   `node_modules` (Node.js dependencies)
*   `target` (Rust build output, Maven build output)
*   `build` (Gradle/Go build output, general build directory)
*   `dist` (Distribution directory for Python, JS)
*   `.DS_Store` (macOS specific file)
*   `Thumbs.db` (Windows specific file)
*   `vendor` (Go dependencies)
*   `coverage` (Coverage reports)
*   `.mypy_cache` (MyPy cache)
*   `.ruff_cache` (Ruff cache)

### ⚠️ Warning

Always use the `--list` option first to review what will be removed. While these patterns are generally safe to delete (as they can be regenerated), unintended data loss can occur if custom patterns are used carelessly. Use `--clean` with caution!
