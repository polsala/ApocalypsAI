### Nightly Commit Chronometer

**Summary:** A GitHub Action that detects 'temporal stasis' by checking the age of the last commit on a branch, flagging or failing if it exceeds a configurable threshold.

This utility helps maintain active development and prevents merging stale branches by providing feedback on the chronological freshness of your commits. It's like a temporal anomaly detector for your codebase!

#### Inputs

*   `max-stasis-days` (required):
    *   **Description**: The maximum number of days a commit can be considered 'fresh'. If the last commit's age exceeds this, temporal stasis is detected.
    *   **Default**: `7`
*   `fail-on-stasis` (optional):
    *   **Description**: If set to `true`, the workflow will fail if temporal stasis is detected. If `false` (default), it will only issue a warning.
    *   **Default**: `false`

#### Outputs

*   `stasis-detected`:
    *   **Description**: `true` if temporal stasis was detected, `false` otherwise.
*   `commit-age-days`:
    *   **Description**: The age of the last commit in days.

#### Usage Example

Add this step to your GitHub Actions workflow (e.g., on `pull_request` or `push`):

```yaml
name: Check Commit Freshness
on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  chronometer_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Nightly Commit Chronometer
        id: chronometer
        uses: polsala/ApocalypsAI/github-actions/nightly-commit-chronometer@main # Replace 'main' with your branch/tag
        with:
          max-stasis-days: 14
          fail-on-stasis: true

      - name: Report Stasis Status
        if: steps.chronometer.outputs.stasis-detected == 'true'
        run: |
          echo "Temporal anomaly detected! Last commit is ${{ steps.chronometer.outputs.commit-age-days }} days old."
        shell: bash

      - name: Continue if no stasis
        if: steps.chronometer.outputs.stasis-detected == 'false'
        run: echo "All clear! Temporal flow is healthy."
        shell: bash
```
