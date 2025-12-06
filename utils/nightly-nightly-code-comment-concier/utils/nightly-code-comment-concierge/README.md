# Nightly Code Comment Concierge

## 🧹 Your Codebase's Personal Assistant for Forgotten Notes

The Nightly Code Comment Concierge is a whimsical-yet-useful utility designed to help maintain the hygiene and clarity of your codebase. It diligently scans specified directories for common developer annotations like `TODO`, `FIXME`, `HACK`, `BUG`, and `NOTE`, compiling them into a comprehensive report.

Never let a temporary `TODO` become a permanent resident of your technical debt again! This tool provides a clear overview of all pending tasks, known issues, and temporary workarounds scattered across your project, making it easier to prioritize and address them.

## ✨ Features

*   **Multi-pattern Scanning**: Detects `TODO`, `FIXME`, `HACK`, `BUG`, and `NOTE` comments by default.
*   **Directory Traversal**: Recursively scans all files in a given directory.
*   **Exclusion Filters**: Allows specifying directories and files to ignore.
*   **Structured Output**: Generates a JSON report for easy programmatic consumption, alongside a human-readable summary.

## 🚀 Usage

To run the Concierge, simply execute the `concierge.py` script with the path to your repository or a specific directory:

```bash
python utils/nightly-code-comment-concierge/src/concierge.py --path ./my_project
```

### Command-line Arguments

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--exclude-dirs <dir1> <dir2> ...`: Space-separated list of directory names to exclude (e.g., `venv .git build`).
*   `--exclude-files <file1> <file2> ...`: Space-separated list of file names to exclude (e.g., `config.py temp.txt`).
*   `--output-format <json|text>`: Specify the output format. Defaults to `text`. `json` provides a machine-readable report.

### Example Output (text format)

```
--- Code Comment Concierge Report ---

Total Findings: 5

File: src/main.py
  L10: TODO: Refactor this spaghetti code into a cleaner function.
  L25: FIXME: This regex is not robust enough for all edge cases.

File: tests/test_feature.py
  L50: HACK: Temporarily disabling this test due to CI issues.

File: docs/roadmap.md
  L5: NOTE: Remember to update the release notes after sprint 3.

File: src/utils.py
  L100: BUG: Division by zero possible here if 'count' is 0.

--- Summary by Type ---
TODO: 1
FIXME: 1
HACK: 1
BUG: 1
NOTE: 1
```

### Example Output (JSON format)

```json
{
  "total_findings": 5,
  "files": [
    {
      "filepath": "src/main.py",
      "findings": [
        {"type": "TODO", "line": 10, "message": "Refactor this spaghetti code into a cleaner function."},
        {"type": "FIXME", "line": 25, "message": "This regex is not robust enough for all edge cases."}
      ]
    },
    {
      "filepath": "tests/test_feature.py",
      "findings": [
        {"type": "HACK", "line": 50, "message": "Temporarily disabling this test due to CI issues."}
      ]
    },
    {
      "filepath": "docs/roadmap.md",
      "findings": [
        {"type": "NOTE", "line": 5, "message": "Remember to update the release notes after sprint 3."}
      ]
    },
    {
      "filepath": "src/utils.py",
      "findings": [
        {"type": "BUG", "line": 100, "message": "Division by zero possible here if 'count' is 0."}
      ]
    }
  ],
  "summary_by_type": {
    "TODO": 1,
    "FIXME": 1,
    "HACK": 1,
    "BUG": 1,
    "NOTE": 1
  }
}
```
