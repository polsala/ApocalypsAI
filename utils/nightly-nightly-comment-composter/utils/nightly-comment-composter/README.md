# Nightly Comment Composter 🧹💬

The Nightly Comment Composter is a whimsical utility designed to help keep your codebase fresh and free of stale, forgotten comments. It scans your Python project for common markers like `TODO`, `FIXME`, `HACK`, and `NOTE`, reporting their locations so you can decide whether to address them, convert them into issues, or finally compost them into oblivion.

## 🌿 Why Compost Comments?

*   **Reduce Technical Debt**: Stale comments often point to unfinished work or known issues that have been neglected.
*   **Improve Code Clarity**: Remove clutter and ensure comments reflect the current state of the code.
*   **Boost Productivity**: Turn forgotten `TODO`s into actionable tasks.

## 🚀 Usage

```bash
python src/composter.py --path <your_project_directory> [--exclude-dirs <dir1> <dir2>] [--exclude-files <file1> <file2>]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--exclude-dirs <dir1> <dir2> ...`: Space-separated list of directory names to exclude from the scan (e.g., `venv .git build`).
*   `--exclude-files <file1> <file2> ...`: Space-separated list of file names to exclude (e.g., `setup.py __init__.py`).

## 🗑️ Example Output

```
Scanning /path/to/your/project...

Found 3 stale comments:
--------------------------------------------------
File: my_module.py, Line: 15
  # TODO: Implement proper error handling for edge cases.
--------------------------------------------------
File: another_script.py, Line: 7
  # FIXME: This regex is inefficient, optimize it later.
--------------------------------------------------
File: utils/helper.py, Line: 30
  # HACK: Temporary workaround for API rate limits. Refactor soon.
--------------------------------------------------

Composting complete! Time to clean up.
```

## 🛠️ Development

The utility is written in Python 3.11.

### Running Tests

```bash
python -m unittest tests/test_composter.py
```
