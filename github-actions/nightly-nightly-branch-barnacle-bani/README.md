# Nightly Branch Barnacle Banishment

## Summary
This GitHub Action helps maintain a tidy repository by identifying branches that haven't been updated in a configurable period (e.g., 60 days) and are not `main`/`master` or explicitly protected. For each 'stale' branch, it takes a whimsical action:

- If an open Pull Request (PR) is associated with the branch, it adds a gentle, whimsical comment to the PR, nudging the author.
- If no open PR exists, it creates a new issue, tagging the last committer, suggesting the branch be reviewed or deleted, with a playful title and body.

This utility aims to reduce repository clutter and remind developers about forgotten work, all with a touch of ApocalypsAI charm.

## Usage
To use the `Nightly Branch Barnacle Banishment` action, add the following workflow file to your repository at `.github/workflows/nightly-branch-barnacle-banishment.yml`.

### Configuration

**Inputs (via `env` variables in the workflow):**

- `STALE_DAYS`: (Optional) The number of days after which a branch is considered stale. Defaults to `60`. (e.g., `STALE_DAYS: 90`)
- `PROTECTED_BRANCHES`: (Optional) A space-separated string of branch names or patterns (e.g., `release/*`) that should always be ignored, even if stale. Defaults to `"main master develop"`.

### Example Workflow

```yaml
name: Nightly Branch Barnacle Banishment

on:
  schedule:
    - cron: '0 3 * * *' # Run daily at 03:00 UTC
  workflow_dispatch: # Allow manual trigger

jobs:
  banish_barnacles:
    runs-on: ubuntu-latest
    permissions:
      contents: read # For git commands
      pull-requests: write # For commenting on PRs
      issues: write # For creating issues
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Fetch all history for accurate branch age

      - name: Install gh CLI (if not present)
        run: | # gh is usually pre-installed on GitHub-hosted runners
          sudo apt-get update && sudo apt-get install -y gh || true

      - name: Run Branch Barnacle Banishment
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          STALE_DAYS: 60 # Configure how many days before a branch is considered stale
          PROTECTED_BRANCHES: "main master develop release/*" # Space-separated list of branches/patterns to ignore
        run: |
          bash "${{ github.workspace }}/github-actions/nightly-branch-barnacle-banishment/src/branch_banisher.sh"
```

## Whimsical Messages

- **PR Comment**: "Psst! This branch, `{{branch_name}}`, seems to be gathering a bit of digital dust. Perhaps it's time to give it some love, merge it, or send it off to the great byte-bin in the sky? Just a friendly whisper from the ApocalypsAI Branch Barnacle Banishment squad!"
- **Issue Title**: "Branch Barnacle Alert! `{{branch_name}}` is feeling neglected."
- **Issue Body**: "Greetings, @{{last_committer}}! The ApocalypsAI Integrator has noticed that the branch `{{branch_name}}` hasn't seen any activity in over {{stale_days}} days. It's looking a bit like a forgotten relic in our digital archives. Could you please take a moment to review its purpose? Perhaps it's ready to be merged, rebased, or gracefully retired? Let's keep our repository sparkling!"
