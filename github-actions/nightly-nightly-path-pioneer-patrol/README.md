# Nightly Path Pioneer Patrol

A GitHub Action designed to enforce the ApocalypsAI repository's V2 classifier-based path structure for new utilities. This action ensures that any newly added utility directories are placed under their appropriate classifier path (e.g., `python-utils/`, `rust-utils/`, `github-actions/`) instead of the legacy `utils/` directory. It also verifies that utility names follow the `nightly-<name>` kebab-case convention.

## Purpose

The ApocalypsAI project is transitioning to a structured utility organization. This action acts as a "patrol" to guide new utility submissions to their correct homes, preventing clutter and ensuring maintainability.

## How it Works

1.  **Identifies New Files**: On a pull request, it scans for newly added files.
2.  **Checks Directory Structure**: For each new file, it determines if it belongs to a new utility directory.
3.  **Enforces V2 Paths**: If a new utility directory is detected, it verifies that it resides under one of the designated V2 classifier paths (e.g., `python-utils/`, `rust-utils/`). It will fail if a new utility is found directly under the legacy `utils/` directory.
4.  **Validates Naming Convention**: It also checks if the utility's directory name starts with `nightly-` and is in kebab-case.

## Usage

Add this action to your workflow, typically on `pull_request` events.

```yaml
name: Path Pioneer Patrol Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  path_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Path Pioneer Patrol
        uses: polsala/ApocalypsAI/github-actions/nightly-path-pioneer-patrol@main # Adjust 'main' to your branch if needed
        id: path_patrol
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-number: ${{ github.event.pull_request.number }}
```

## Inputs

*   `github-token`:
    *   **Description**: GitHub token for API access (e.g., `secrets.GITHUB_TOKEN`). Required to fetch PR file changes.
    *   **Required**: `true`
*   `pr-number`:
    *   **Description**: The pull request number.
    *   **Required**: `true`

## Outputs

None directly, but the action will fail if path violations are detected.

## Development & Testing

The core logic is implemented in `src/check_paths.sh`. Tests are located in `tests/test_check_paths.sh` and can be run locally.
