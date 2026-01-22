# Emoji Issue Welcome Action

This GitHub Action posts a whimsical emoji welcome comment whenever a new issue is opened. It selects an emoji deterministically based on the issue number, ensuring repeatable results.

## Usage

```yaml
name: Issue Welcome

on:
  issues:
    types: [opened]

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-emoji-issue-welcome
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action reads the `issue` payload from `GITHUB_EVENT_PATH`, picks an emoji from a predefined list using `issue_number % len(emojis)`, and posts a comment via the GitHub REST API.
