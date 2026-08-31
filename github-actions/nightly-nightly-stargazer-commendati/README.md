# Nightly Stargazer Commendation

A GitHub Action that randomly selects a recently merged Pull Request and adds a whimsical, star-themed comment to commend the contribution. This utility aims to boost team morale and acknowledge the hard work of contributors in a fun, unexpected way.

## How it Works

1.  **Fetches Merged PRs**: The action queries the GitHub API for Pull Requests that have been merged within a specified number of days.
2.  **Random Selection**: From the list of eligible merged PRs, one is randomly chosen.
3.  **Whimsical Commendation**: A pre-defined, whimsical, star-themed comment is posted to the selected Pull Request.

## Usage

To use this action, add a step to your GitHub Actions workflow. It's typically run on a schedule, for example, nightly.

```yaml
name: Stargazer Commendation Nightly

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch:

jobs:
  commend_pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Stargazer Commendation
        # Replace with the actual path to this action in the repository
        # e.g., uses: polsala/ApocalypsAI/nightly-stargazer-commendation@main
        uses: ./nightly-stargazer-commendation # For local testing or if action is in same repo
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          days-back: 7 # Look for PRs merged in the last 7 days
```

## Inputs

*   `github-token`: **Required**. A GitHub token with `pull_requests: write` and `issues: write` permissions. Typically, `${{ secrets.GITHUB_TOKEN }}` is sufficient.
*   `days-back`: **Optional**. The number of days to look back for merged Pull Requests. Defaults to `7`.

## Outputs

None.

## Development

This action is written in JavaScript. Dependencies are managed via `npm`.

To run tests:

```bash
npm install
npm test
```
