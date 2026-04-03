# Emoji Stale Label Action

A whimsical GitHub Action that adds a fun emoji label to issues and pull requests that have been inactive for a configurable number of days. Perfect for drawing attention to forgotten items in a playful way.

## Inputs

- `days` (default: `30`) – Number of days of inactivity after which the label is applied.
- `label` (default: `stale`) – The base label name to use.
- `emoji` (default: `🧟`) – Emoji to prepend to the label.

## How it works

The action reads the event payload (`GITHUB_EVENT_PATH`) to determine the issue or PR number and its `updated_at` timestamp. If the item has been inactive for at least `days`, it prints a message indicating that it would add the label `<emoji> <label>`.

> **Note:** This action only prints a message; it does not actually call the GitHub API. It is intended as a demonstration or can be extended to perform real labeling.

## Usage

```yaml
name: Stale Issue Emoji Label

on:
  schedule:
    - cron: '0 0 * * *' # daily

jobs:
  label-stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./ # uses this action
        with:
          days: 14
          label: 'needs-attention'
          emoji: '⚠️'
```

## License

MIT
