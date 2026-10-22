# Nightly Utility Structure Validator

This GitHub Action ensures that newly added utilities adhere to the ApocalypsAI repository's `AGENTS.md` guidelines for directory structure and essential files. It's like a digital Sentry Bot, making sure every new contribution is properly organized for the post-apocalyptic codebase.

## Purpose

The ApocalypsAI project thrives on structured chaos. While agents are free to invent, their creations must be well-documented and testable. This action automates the validation of new utility directories, checking for:
- The existence of the utility's root directory.
- A `README.md` file at the root.
- A `src/` directory containing at least one source file.
- A `tests/` directory containing at least one test file.

## Usage

To use this action in your workflow, provide the path to the utility you wish to validate.

```yaml
name: Validate New Utility PR
on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - '**/nightly-*/**' # Trigger when any new utility path is touched

jobs:
  validate-utility-structure:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Find new utility path (example for a single new utility)
        id: find_util_path
        run: |
          # This is a simplified example. In a real scenario, you might parse
          # git diff to find the exact new utility path. For instance, if a PR
          # adds `python-utils/nightly-my-new-tool/README.md` and other files,
          # you'd extract `python-utils/nightly-my-new-tool`.
          # For demonstration, let's assume the PR adds a utility at 'python-utils/nightly-example-tool'
          echo "util_path=python-utils/nightly-example-tool" >> "$GITHUB_OUTPUT"
          # A more robust solution would iterate through changed files and identify new utility roots.
          # Example using git diff:
          # NEW_FILES=$(git diff --name-only --diff-filter=A ${{ github.event.pull_request.base.sha }} ${{ github.sha }})
          # FIRST_NEW_UTIL_PATH=$(echo "$NEW_FILES" | grep -oE '^[a-z-]+/nightly-[a-z0-9-]+/' | head -n 1)
          # if [ -n "$FIRST_NEW_UTIL_PATH" ]; then
          #   echo "util_path=$FIRST_NEW_UTIL_PATH" >> "$GITHUB_OUTPUT"
          # else
          #   echo "No new utility path found in this PR, skipping validation."
          #   exit 0
          # fi

      - name: Validate Utility Structure
        if: steps.find_util_path.outputs.util_path != ''
        uses: ./github-actions/nightly-util-struct-validator # Path to this action
        with:
          util-path: ${{ steps.find_util_path.outputs.util_path }}
```

## Inputs

### `util-path`
**Required** The path to the utility directory to validate (e.g., `python-utils/nightly-my-tool`).

## Outputs

None. The action will fail if validation checks do not pass.

## Development

The core logic resides in `src/validate_util_structure.sh`. Tests are in `tests/test_validate_util_structure.sh`.
