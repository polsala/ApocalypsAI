# Nightly Repository Prognosticator

## Overview

The `nightly-repo-prognosticator` is a whimsical yet practical utility designed to scan your local Git repository for key health indicators and provide a 'cosmic prognosis' on its state. It helps maintainers keep an eye on potential issues like stale branches and inactivity, all wrapped in a delightful, apocalyptic-themed report.

## Features

*   **Stale Branch Detection**: Identifies local branches that haven't been updated in a configurable number of days.
*   **Recent Activity Check**: Reports the last commit date on the main development branch (`main` or `master`).
*   **Whimsical Prognosis**: Generates a fun, themed message based on the repository's health metrics.
*   **Self-contained**: Operates purely on the local Git repository using standard `git` commands.

## Usage

To run the prognosticator, navigate to the root of your Git repository and execute the script:

```bash
# From the repository root:
python utils/nightly-repo-prognosticator/src/prognosticator.py [--stale-days <days>] [--main-branch <branch_name>]
```

*   `--stale-days`: (Optional) Number of days after which a branch is considered stale. Defaults to `90`.
*   `--main-branch`: (Optional) The name of your main development branch (e.g., `main`, `master`). Defaults to `main`.

### Example Output

```
🌌 Repository Prognosis Report 🌌

--- Health Metrics ---
Last commit on 'main': Thu Oct 26 10:30:00 2023 +0000
Stale branches (older than 90 days):
  - feature/old-feature (last commit: 2023-05-15)
  - bugfix/forgotten-fix (last commit: 2023-04-01)

--- Cosmic Prognosis ---
Warning: A nebula of forgotten branches is forming. Initiate immediate stellar cleanup protocols!
```

## Development

This utility is written in Python and relies on `subprocess` calls to `git`.

### Running Tests

To run the tests, navigate to the `utils/nightly-repo-prognosticator/` directory and execute:

```bash
python -m unittest tests/test_prognosticator.py
```
