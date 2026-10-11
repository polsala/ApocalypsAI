# Nightly Utility Path Patrol

The ApocalypsAI Nightly Integrator agent ensures that all new utilities added to the repository adhere to the strict V2 classifier-based path and naming conventions. This action acts as a vigilant "Path Patrol," automatically checking Pull Requests for compliance.

## Purpose

This GitHub Action is designed to:
- Validate that new utility directories are placed under a valid V2 classifier path (e.g., `python-utils/`, `rust-utils/`, `github-actions/`).
- Ensure that utility directory names start with the `nightly-` prefix.
- Verify that the utility name (after `nightly-`) is in kebab-case and the full utility directory name (e.g., `nightly-my-util`) does not exceed 32 characters.
- Confirm the presence of essential files/directories (`README.md`, `src/`, `tests/`) within each new utility.

By enforcing these standards, the `nightly-util-path-patrol` helps maintain repository organization and consistency, making it easier for agents and humans alike to navigate and contribute.

## Usage

To use this action in your workflow, add a step that calls `nightly-util-path-patrol` in your Pull Request workflow.

```yaml
name: Validate New Utilities

on:
  pull_request:
    branches:
      - main # Or your default branch

jobs:
  validate_utilities:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Important: Needed for git diff to compare base and head

      - name: Run Nightly Utility Path Patrol
        uses: polsala/ApocalypsAI/github-actions/nightly-util-path-patrol@main # Adjust path if this action is moved
        id: patrol
        with:
          base_sha: ${{ github.event.pull_request.base.sha }}
          head_sha: ${{ github.event.pull_request.head.sha }}

      - name: Report Validation Status
        run: |
          echo "Utility path validation status: ${{ steps.patrol.outputs.validation_status }}"
          if [ "${{ steps.patrol.outputs.validation_status }}" == "failure" ]; then
            echo "::error::New utility paths failed validation. Please check the logs above."
            exit 1
          fi
```

### Inputs

| Name        | Description                                     | Required |
| :---------- | :---------------------------------------------- | :------- |
| `base_sha`  | The base SHA of the pull request.               | `true`   |
| `head_sha`  | The head SHA of the pull request.               | `true`   |

### Outputs

| Name                | Description                                     |
| :------------------ | :---------------------------------------------- |
| `validation_status` | The status of the validation (`success`, `failure`, or `skipped`). |

## Development & Testing

The action includes a `tests/test.yml` workflow that simulates various PR scenarios (valid and invalid utility additions) to ensure the validation logic works as expected. This test workflow creates a temporary git repository with a controlled history, allowing for deterministic and offline testing of the `git diff` commands used by the action.
