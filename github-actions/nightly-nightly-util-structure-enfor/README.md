# Nightly Util Structure Enforcer

This GitHub Action ensures that all utility folders within the `polsala/ApocalypsAI` repository adhere to the required structural standards: each utility must contain a `README.md` file, a `src/` directory, and a `tests/` directory.

This action is crucial for maintaining the "Anarchy with discipline" philosophy, ensuring that while agents are free to create diverse utilities, they all conform to a baseline of discoverability and testability.

## Usage

To use this action in your workflow, you can reference it directly from the repository. It takes one input: `util-path`.

```yaml
name: Check Utility Structure on PR

on:
  pull_request:
    branches:
      - main
    paths:
      - '**/README.md'
      - '**/src/**'
      - '**/tests/**'

jobs:
  check_util_structure:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Extract changed utility paths
        id: changed_paths
        run: |
          # This step would typically use git diff to find changed utility paths.
          # For demonstration, let's assume a single path is being checked.
          # In a real scenario, you'd parse `git diff --name-only` output.
          echo "util_path=python-utils/my-new-util" >> $GITHUB_OUTPUT
          # Mock rationale: In a real PR workflow, this would dynamically determine
          # the utility paths affected by the PR. For this README example, we use a placeholder.

      - name: Enforce Utility Structure
        uses: polsala/ApocalypsAI/github-actions/nightly-util-structure-enforcer@main # Adjust path if action is moved
        with:
          util-path: ${{ steps.changed_paths.outputs.util_path }}
```

### Inputs

- `util-path`: **Required**. The relative path to the utility folder to check (e.g., `python-utils/my-whimsical-tool`).

### Outputs

- `status`: The status of the structure check. `valid` if the structure is correct, `invalid` otherwise.

## How it Works

The action's core logic is a simple bash script that checks for the existence of `README.md`, `src/`, and `tests/` within the provided `util-path`. If any are missing, it logs an error and fails the step. If the `util-path` itself does not exist (e.g., a utility is being deleted), it issues a warning and passes, as there's no structure to enforce.
