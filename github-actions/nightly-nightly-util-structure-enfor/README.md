# Nightly Utility Structure Enforcer

A GitHub Action designed to enforce the ApocalypsAI repository's utility structure guidelines. It automatically checks any newly added utility directories within specified classifier paths (e.g., `python-utils/`, `rust-utils/`, `utils/`) to ensure they contain both a `README.md` file and a `tests/` subdirectory.

This action helps maintain consistency, testability, and documentation across all community-contributed utilities, aligning with the "Isolation & tests" and "Self-contained utilities" philosophies.

## Usage

To use this action, add it as a step in your GitHub Actions workflow, typically on `pull_request` events targeting the `main` branch.

```yaml
name: Enforce Utility Structure

on:
  pull_request:
    branches:
      - main

jobs:
  check_utility_structure:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required to compare against the base branch

      - name: Enforce Utility Structure
        # Use a relative path if the action is in the same repository
        uses: ./github-actions/nightly-util-structure-enforcer@main 
        with:
          # Optional: Customize the paths where new utilities are expected.
          # Defaults to all V2 classifier paths and the legacy 'utils/' path.
          # check-paths: "utils/,python-utils/,rust-utils/"
```

## Inputs

*   `check-paths` (Optional): A comma-separated string of parent directories where new utilities are expected. The action will look for new subdirectories within these paths. Defaults to all V2 classifier paths and the legacy `utils/` path.

## How it Works

1.  **Checkout Repository**: The action first checks out the repository, fetching the full history to allow for accurate diffing.
2.  **Identify New Files**: It uses `git diff` to identify all files that have been newly added (`--diff-filter=A`) in the current pull request compared to its base branch.
3.  **Discover New Utility Directories**: From the list of new files, it determines which unique parent directories fall under the configured `check-paths` (e.g., `python-utils/my-new-util/`). These are considered new utility directories.
4.  **Enforce Structure**: For each identified new utility directory, it verifies the presence of:
    *   A `README.md` file directly within the utility's root directory.
    *   A `tests/` subdirectory directly within the utility's root directory.
5.  **Report and Fail**: If any required file or directory is missing, the action will log an error and fail the workflow, preventing the merge of non-compliant utilities.
