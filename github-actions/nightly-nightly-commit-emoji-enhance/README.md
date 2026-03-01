# Nightly Commit Emoji Enhancer

A reusable GitHub Actions workflow that adds a random emoji to the title of a pull request when the workflow is triggered. Great for adding a touch of whimsy to your PRs.

## Usage

Create a workflow in your repository that calls this reusable workflow:

```yaml
name: Add Emoji to PR Title
on:
  pull_request:
    types: [opened, edited]

jobs:
  enhance:
    uses: your-org/ApocalypsAI/.github/workflows/nightly-commit-emoji-enhancer.yml@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope to edit PR titles.

## How it works

The workflow runs a JavaScript snippet via `actions/github-script` that selects a random emoji from a predefined list and prepends it to the PR title.
