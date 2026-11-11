# Nightly Path Patrol

This GitHub Action acts as a vigilant guardian, ensuring that all new utilities integrated into the ApocalypsAI repository adhere to the established V2 classifier-based path structure. It checks for the presence of essential files and directories (`README.md`, `src/`, `tests/`) within newly added utility folders and verifies the `nightly-` prefix for utility names.

## Purpose

The ApocalypsAI project thrives on structured chaos. While agents are free to invent, their creations must be well-organized and self-contained. This action automates the enforcement of these structural guidelines, catching common errors early in the Pull Request lifecycle.

## How it Works

When a Pull Request is opened or updated, this action will:

1.  Identify any newly added directories that resemble a utility (e.g., `python-utils/nightly-my-tool/`, `utils/nightly-legacy-tool/`).
2.  For each detected new utility directory, it performs the following checks:
    *   **Name Prefix**: Ensures the utility directory name starts with `nightly-`.
    *   **README**: Verifies the existence of a `README.md` file at the utility's root.
    *   **Source Code**: Confirms the presence of a non-empty `src/` subdirectory.
    *   **Tests**: Confirms the presence of a non-empty `tests/` subdirectory.
3.  If any of these checks fail, the action will mark the PR check as failed and output detailed error messages, guiding the contributor to fix the structure.

## Usage

To use the Nightly Path Patrol in your workflow, add it as a step in your `.github/workflows/*.yml` file, typically on `pull_request` events.

```yaml
name: Validate Utility Paths
on:
  pull_request:
    branches:
      - main

jobs:
  validate-paths:
    runs-on: ubuntu-latest
    steps:
      - name: Nightly Path Patrol
        uses: polsala/ApocalypsAI/.github/actions/nightly-path-patrol@main # Adjust path if this action is moved
        with:
          pr-number: ${{ github.event.pull_request.number }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

*   `pr-number` (Required): The number of the Pull Request to validate. This is typically `${{ github.event.pull_request.number }}`.
*   `github-token` (Required): A GitHub token with `pull_requests: read` permissions. This is typically `${{ secrets.GITHUB_TOKEN }}`.

## Development & Testing

The core logic resides in `src/path_validator.sh`. Tests are implemented in `tests/test_path_validator.sh` using a mocked `gh` CLI to ensure deterministic and offline execution.
