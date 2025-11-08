# Apocalypse Asset Auditor

## Overview

The `Apocalypse Asset Auditor` is a crucial utility for the ApocalypsAI collective, designed to ensure that every repository is prepared for the inevitable digital cataclysm. It scans a given repository path for essential 'survival kit' assets – key files and directories that are vital for a project's health, compliance, and operational integrity.

Think of it as checking your emergency bunker for supplies: Is the README present? Is the LICENSE valid? Are the core agent contracts (`AGENTS.md`) and automation blueprints (`.github/workflows/`) in place?

## Features

*   **Critical Asset Check**: Verifies the existence of `README.md`, `LICENSE`, `AGENTS.md`, and the `.github/workflows/` directory.
*   **Basic Health Assessment**: Reports if files are present but empty, or if the `LICENSE` file contains common placeholder text.
*   **JSON Output**: Provides a structured report for easy integration with other tools or agents.

## Usage

To run the auditor, provide the path to the repository you wish to inspect:

```bash
python src/auditor.py --repo-path /path/to/your/repository
```

### Example Output (JSON)

```json
{
  "repo_path": "/path/to/your/repository",
  "status": "healthy",
  "assets": {
    "README.md": {
      "exists": true,
      "empty": false,
      "status": "ok"
    },
    "LICENSE": {
      "exists": true,
      "empty": false,
      "placeholder": false,
      "status": "ok"
    },
    "AGENTS.md": {
      "exists": true,
      "empty": false,
      "status": "ok"
    },
    ".github/workflows/": {
      "exists": true,
      "empty": false,
      "status": "ok"
    }
  },
  "issues": []
}
```

## Development

This utility is written in Python 3.11 and is self-contained. Tests are located in `tests/test_auditor.py` and use `unittest.mock` for deterministic, offline execution.
