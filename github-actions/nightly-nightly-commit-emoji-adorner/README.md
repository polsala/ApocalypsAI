# Commit Emoji Adorner

A whimsical GitHub Action that adds a random emoji comment to every new pull request, spreading joy across your repository.

## Usage

```yaml
name: Add Emoji to PRs
on:
  pull_request:
    types: [opened]

jobs:
  emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/commit-emoji-adorner
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `token` (required) – GitHub token with `repo` scope.

## Outputs

- `comment` – The exact comment that was posted.

## How it works

The action picks a random emoji from a curated list and posts a friendly comment on the PR.
