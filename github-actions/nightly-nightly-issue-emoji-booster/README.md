# Nightly Issue Emoji Booster

A GitHub Action that automatically adds a random emoji reaction to newly opened issues, spreading a bit of joy.

## How it works

When an issue is opened, the action selects a random emoji from a curated list and posts it as a reaction via the GitHub API.

## Usage

Add the following step to your workflow (or copy the example workflow below).

```yaml
name: Issue Emoji Booster

on:
  issues:
    types: [opened]

jobs:
  emoji-booster:
    runs-on: ubuntu-latest
    steps:
      - name: Add emoji reaction
        uses: ./\.github\-actions/nightly-issue-emoji-booster
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Example workflow

```yaml
name: Nightly Issue Emoji Booster

on:
  issues:
    types: [opened]

jobs:
  boost:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run Emoji Booster
        uses: ./.github-actions/nightly-issue-emoji-booster
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## License

MIT
