# Nightly PR Pep Talk

This GitHub Action provides a whimsical yet encouraging nudge to Pull Requests that have been inactive for a specified period. It's designed to gently remind contributors about their open PRs, fostering a sense of community and continuous progress, even in the face of the apocalypse.

## Features

- **Inactivity Detection**: Checks the `updatedAt` timestamp of a PR against a configurable inactivity threshold.
- **Whimsical Messages**: Generates a random, encouraging message from a predefined list.
- **Configurable Prefix**: Allows customization of the comment's prefix.

## Usage

To use this action, add it as a step in your GitHub Actions workflow. It's ideal for a scheduled workflow that runs periodically (e.g., daily or weekly) to find and process multiple PRs.

### `.github/workflows/scheduled-pr-pep-talk.yml` (Example Dispatcher Workflow)

This example shows how to set up a scheduled workflow that finds all open PRs and then dispatches the `nightly-pr-pep-talk` action for each of them using a matrix strategy.

```yaml
name: Scheduled PR Pep Talk Dispatcher

on:
  schedule:
    - cron: '0 8 * * *' # Run daily at 8 AM UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  find-and-dispatch:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read # To list PRs
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install gh CLI (if not already present)
        run: |
          if ! command -v gh &> /dev/null
          then
              echo "gh CLI not found, installing..."
              sudo apt-get update
              sudo apt-get install -y gh
          fi

      - name: List open PRs
        id: list_prs
        run: |
          # Get PR numbers of open PRs and format as JSON array for matrix strategy
          PR_NUMBERS=$(gh pr list --state open --json number --jq '.[].number')
          echo "Found PRs: $PR_NUMBERS"
          echo "prs=$(echo $PR_NUMBERS | jq -R 'split("\n") | map(select(length > 0))' )" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  pep-talk-each-pr:
    needs: find-and-dispatch
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required by the called action to comment
      contents: read

    strategy:
      matrix:
        pr_number: ${{ fromJson(needs.find-and-dispatch.outputs.prs) }}

    steps:
      - name: Give pep talk to PR ${{ matrix.pr_number }}
        # Use the action from the current repository and branch
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-pep-talk@main # Adjust to your branch/tag
        with:
          pr-number: ${{ matrix.pr_number }}
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          inactivity-days: 7 # Default is 7 days, can be customized
          comment-prefix: 'ApocalypsAI Integrator whispers:' # Default prefix, can be customized
```

## Inputs

| Name            | Description                                  | Required | Default       |
|-----------------|----------------------------------------------|----------|---------------|
| `pr-number`     | The number of the Pull Request to check.     | Yes      |               |
| `repo-token`    | GitHub token with `pull-requests: write` permissions. | Yes      |               |
| `inactivity-days` | Number of days after which a PR is considered inactive. | No       | `7`           |
| `comment-prefix`  | Prefix for the pep talk comment.             | No       | `ApocalypsAI Integrator whispers:` |

## Outputs

| Name        | Description                                  |
|-------------|----------------------------------------------|
| `commented` | `true` if a comment was added, `false` otherwise. |
