# Nightly Survival Kit Checker

**Ensuring your project is apocalypse-ready, one file at a time!**

## 🚀 Overview

In the chaotic aftermath of a digital apocalypse, the last thing you need is a project missing its vital components. The `Nightly Survival Kit Checker` is your vigilant guardian, scanning specified directories to ensure all essential files are present and accounted for. Think of it as a pre-flight checklist for your codebase, making sure your project can withstand any unforeseen digital fallout.

It helps maintain project hygiene, ensures new contributors have all necessary setup files, and prevents critical omissions that could lead to system collapse (or just a really bad day).

## ✨ Features

*   **Configurable Essential Files**: Define your own list of critical files (e.g., `README.md`, `LICENSE`, `.gitignore`, `requirements.txt`, `.env`).
*   **Directory Scanning**: Scans a target directory for the presence of these files/directories.
*   **Clear Reporting**: Provides a summary of present and missing essential items.
*   **Whimsical Output**: Delivers results with a touch of post-apocalyptic charm.

## 🛠️ Usage

### Prerequisites

*   Python 3.8+

### Installation (Standalone)

This utility is designed to be self-contained. Simply navigate into its directory.

### Running the Checker

```bash
python src/checker.py --path /path/to/your/project
```

**Options:**

*   `--path <directory>`: The root directory of the project to check. (Required)
*   `--files <item1,item2,...>`: A comma-separated list of essential files/directories to look for. Defaults to `README.md,LICENSE,.gitignore,requirements.txt,.env`.
*   `--verbose`: Show more detailed output, including present files.

### Example

```bash
# Check a project with default essential files
python src/checker.py --path ./my_awesome_project

# Check with custom files and verbose output
python src/checker.py --path ./my_awesome_project --files "config.py,data/,models/" --verbose
```

## 🧪 Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_checker.py
```

This will run a suite of deterministic, offline tests to ensure the checker is always ready for duty.
