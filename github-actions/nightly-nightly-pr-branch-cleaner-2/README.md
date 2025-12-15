# Nightly PR Branch Cleaner

A whimsical GitHub Action that says goodbye to stale merged branches. It scans the repository for branches whose pull requests have been merged and are older than a configurable number of days, then deletes them with a friendly farewell message.

## Inputs

- `github_token` (required): A token with `repo` scope to call the GitHub API.
- `days_old` (optional, default `30`): Minimum age in days for a merged branch to be considered stale.

## Usage

```yaml
name: Clean up stale branches
on:
  schedule:
    - cron: '0 3 * * *' # daily at 03:00 UTC
jobs:
  prune:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Prune stale merged branches
        uses: ./github-actions/nightly-pr-branch-cleaner
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          days_old: 14
```

The action will log each deleted branch with a whimsical message like “🗑️ Farewell, `feature/old‑idea`! May your code rest in peace.”

## How it works

1. List all branches via the GitHub API.
2. For each branch, find the associated pull request.
3. If the PR is merged and the branch’s `commit.author.date` is older than `days_old`, delete the branch.
4. Output a friendly message for each deletion.

## Testing

Run the provided test script locally:

```bash
bash tests/test_cleanup.sh
```

The test uses mocked API responses and does not require network access.
