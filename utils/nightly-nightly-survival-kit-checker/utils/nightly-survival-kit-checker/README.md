# Nightly Survival Kit Checker

## 📦 `utils/nightly-survival-kit-checker`

The ApocalypsAI Nightly Survival Kit Checker is a whimsical-yet-useful utility designed to ensure your repository is always prepared for the unexpected. It scans a specified directory for a list of essential "survival kit" files (like `README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `SECURITY.md`) and provides a quick report on their presence or absence, along with a "survival readiness" score.

Maintaining these foundational files is crucial for project health, collaboration, and legal compliance, even in the most chaotic of digital apocalypses.

### ✨ Features

*   **Essential File Scan**: Checks for common, critical repository files.
*   **Customizable Kit**: Define your own list of "essential" files.
*   **Survival Score**: Get a clear `X/Y` score indicating your repository's readiness.
*   **Clear Reporting**: Lists present and missing files for easy action.
*   **Whimsical Theme**: Because even the end of the world needs a little fun.

### 🚀 Usage

To run the Survival Kit Checker, navigate to its directory and execute the `checker.py` script with the target directory as an argument.

```bash
python3 src/checker.py <path_to_repository>
```

**Example: Check the current directory with default files**

```bash
python3 src/checker.py .
```

**Example: Check a specific directory with custom files**

```bash
python3 src/checker.py /path/to/your/project --files README.md LICENSE .env.example
```

### ⚙️ Arguments

*   `<directory>` (required): The path to the repository directory you want to check.
*   `--files` (optional): A space-separated list of file names to check for. If not provided, it defaults to `README.md LICENSE .gitignore CONTRIBUTING.md SECURITY.md`.

### 📊 Output

The utility will print a report to the console, indicating the status, score, and lists of present and missing files.

```
Checking survival kit for directory: .
Required files: README.md, LICENSE, .gitignore, CONTRIBUTING.md, SECURITY.md

--- Survival Kit Report ---
Status: NEEDS ATTENTION
Score: 3/5
Present files: README.md, LICENSE, .gitignore
Missing files: CONTRIBUTING.md, SECURITY.md
--------------------------
```

An exit code of `0` indicates all required files were found (`READY` status). An exit code of `1` indicates missing files (`NEEDS ATTENTION` or `DIRECTORY NOT FOUND` status).

### 🧪 Testing

To run the tests for the Survival Kit Checker, execute the `test_checker.py` script using `unittest`:

```bash
python3 -m unittest tests/test_checker.py
```

All tests are designed to be deterministic and run offline using mocks for file system operations.
