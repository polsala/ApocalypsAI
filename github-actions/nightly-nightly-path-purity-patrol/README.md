# Nightly Path Purity Patrol

## Overview
The `nightly-path-purity-patrol` is a GitHub Action designed to enforce the ApocalypsAI repository's V2 utility path structure. It scans newly added files in a Pull Request and flags any that are incorrectly placed within the legacy `utils/` directory, ensuring all new utilities are organized under their respective classifier-based directories (e.g., `python-utils/`, `rust-utils/`).

This action helps maintain a clean and organized repository, preventing the accidental reintroduction of utilities into the deprecated `utils/` path.

## How it Works
1. The action receives a newline-separated list of newly added file paths (typically from `git diff --name-only --diff-filter=A`).
2. It iterates through these paths, checking if any of them start with `utils/`.
3. If a file path starts with `utils/`, it's considered a violation of the V2 pathing standard.
4. The action outputs a boolean `is_pure` (true if no violations, false otherwise) and a `violations` string listing all non-compliant paths.

## Usage
To use this action in your workflow, typically within a Pull Request check:

```yaml
name: 'Enforce V2 Utility Paths'

on:
  pull_request:
    branches:
      - main

jobs:
  check_utility_paths:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Get added files
        id: added_files
        run: |
          echo "added_files=$(git diff --name-only --diff-filter=A ${{ github.event.pull_request.base.sha }} ${{ github.sha }})" >> "$GITHUB_OUTPUT"
        shell: bash

      - name: Run Path Purity Patrol
        id: path_patrol
        uses: ./github-actions/nightly-path-purity-patrol # Path to the action within the repository
        with:
          added_files: ${{ steps.added_files.outputs.added_files }}

      - name: Report violations
        if: ${{ !steps.path_patrol.outputs.is_pure }}
        run: |
          echo "::error::Found non-compliant utility paths! Please move these files to their respective V2 classifier directories (e.g., python-utils/, rust-utils/)."
          echo "Violations found:\n${{ steps.path_patrol.outputs.violations }}"
          exit 1
```

## Inputs
- `added_files`: (Required) A newline-separated string of newly added file paths. This should typically be generated using `git diff --name-only --diff-filter=A` in your workflow.

## Outputs
- `is_pure`: `true` if all added files are V2 compliant; `false` otherwise.
- `violations`: A newline-separated string listing all newly added file paths that violate the V2 pathing standard.
