# Nightly Cosmic Alignment Checker

This GitHub Action acts as a whimsical-yet-useful gatekeeper for your workflows, ensuring that all 'cosmic' conditions are met before proceeding. It allows you to define a set of checks based on the current branch, the latest commit message, the day of the week, or the presence of specific environment variables.

Prevent accidental deployments on forbidden days, ensure critical phrases are in commit messages, or enforce specific branch patterns with a touch of celestial guidance.

## Features

*   **Branch Pattern Matching**: Define a regex pattern for allowed branch names.
*   **Commit Message Phrase**: Require a specific phrase to be present in the latest commit message.
*   **Forbidden Day of Week**: Block workflows on certain days (e.g., no deployments on Fridays!).
*   **Required Environment Variable**: Ensure a specific environment variable is set to `true`.
*   **Clear Outputs**: Provides `alignment_status` ("aligned" or "misaligned") and a `reason` for its decision.

## Usage

Add this action to your GitHub Workflow (`.github/workflows/your-workflow.yml`):

```yaml
name: Deploy on Cosmic Alignment

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  check_alignment_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 1 # Required for git log to get commit message

      - name: Set Cosmic Blessing (example env var)
        run: echo "COSMIC_BLESSING=true" >> $GITHUB_ENV
        # Mock rationale: This step simulates setting an environment variable that the action might check.
        # In a real scenario, this could come from a previous step, secrets, or other dynamic sources.

      - name: Check Cosmic Alignment
        id: cosmic_check
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-alignment-checker@main # Replace 'main' with your branch/tag
        with:
          required_branch_pattern: '^main$|^release/.*$'
          required_commit_phrase: '🚀 Ready for launch!'
          forbidden_day_of_week: 'Friday'
          required_env_var_name: 'COSMIC_BLESSING'

      - name: Proceed with Deployment if Aligned
        if: steps.cosmic_check.outputs.alignment_status == 'aligned'
        run: |
          echo "Cosmic alignment achieved! Deploying..."
          # Your deployment commands here

      - name: Halt Deployment if Misaligned
        if: steps.cosmic_check.outputs.alignment_status == 'misaligned'
        run: |
          echo "Cosmic misalignment detected: ${{ steps.cosmic_check.outputs.reason }}"
          exit 1 # Fail the job

```

### Inputs

*   `required_branch_pattern` (optional, default: `.*`)
    *   A regex pattern that the current branch name must match. E.g., `^main$|^release/.*$`.
*   `required_commit_phrase` (optional, default: `''`)
    *   A specific substring that must be present in the latest commit message. E.g., `🚀 Ready for launch!`.
*   `forbidden_day_of_week` (optional, default: `''`)
    *   A specific day of the week (e.g., `Friday`) on which the workflow is forbidden. Case-sensitive.
*   `required_env_var_name` (optional, default: `''`)
    *   The name of an environment variable that must be set to the string `true` for alignment. E.g., `COSMIC_ALIGNMENT_STATUS`.

### Outputs

*   `alignment_status`
    *   `aligned` if all conditions are met, `misaligned` otherwise.
*   `reason`
    *   A descriptive message indicating why the alignment status was determined.

## Development & Testing

The core logic resides in `src/check_alignment.sh`. Tests for this script are located in `tests/test_check_alignment.sh` and can be run locally without a GitHub Actions runner:

```bash
cd github-actions/nightly-cosmic-alignment-checker/tests
bash test_check_alignment.sh
```

These tests mock environment variables that would normally be provided by the GitHub Actions runner or `git` commands, ensuring deterministic and offline execution.
