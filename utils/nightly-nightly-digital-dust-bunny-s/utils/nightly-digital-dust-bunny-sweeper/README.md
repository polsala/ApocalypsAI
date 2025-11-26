# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-powerful utility designed to keep your repository sparkling clean by automatically sweeping away common build caches and temporary files. Think of it as a tiny, diligent robot vacuum for your project's digital clutter!

Regularly removing these "dust bunnies" (like `__pycache__`, `.pytest_cache`, `node_modules`, `target/`, `build/`, `dist/`) helps:
*   **Free up disk space:** Essential for constrained CI/CD environments and local development.
*   **Ensure clean builds:** Prevents stale artifacts from causing unexpected issues.
*   **Improve repository hygiene:** Keeps your project lean and focused.

## 🚀 Usage

Navigate to your project's root directory and run the sweeper:

```bash
python src/sweeper.py --path .
```

### Options:

*   `--path <directory>`: Specify the root directory to scan. Defaults to the current working directory (`.`).
*   `--dry-run`: Perform a scan and report what *would* be deleted, without actually removing any files. This is highly recommended for a first run!

### Examples:

**1. Dry run in the current directory (recommended first step):**

```bash
python src/sweeper.py --dry-run
```

**2. Clean a specific project directory:**

```bash
python src/sweeper.py --path /path/to/your/project
```

**3. Perform a full sweep (deletes files!):**

```bash
python src/sweeper.py
```

## 🛠️ Development

### Supported Dust Bunnies:

The sweeper currently targets the following common directories/patterns:
*   `__pycache__` (Python bytecode cache)
*   `.pytest_cache` (pytest cache)
*   `.mypy_cache` (mypy type checker cache)
*   `build` (Python build artifacts)
*   `dist` (Python distribution packages)
*   `node_modules` (Node.js dependencies)
*   `target` (Rust build artifacts, sometimes used in other contexts)

### Adding New Patterns:

To extend the sweeper, modify the `self.patterns` list in `src/sweeper.py` to include new directories or file patterns you wish to clean.

## 🧪 Testing

To run the tests, navigate to the utility's root directory (`utils/nightly-digital-dust-bunny-sweeper/`) and execute:

```bash
python -m unittest tests/test_sweeper.py
```

The tests use `unittest.mock` to simulate file system operations, ensuring they are deterministic and do not actually delete files on your system.
