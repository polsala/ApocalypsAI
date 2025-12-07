# Nightly PR Branch Cleaner

A tiny GitHub Action that scans a repository for branches that have been merged into the default branch and are older than a configurable number of days, then deletes them.  This helps keep the repository clean and prevents branch clutter.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `days_to_keep` | Number of days to retain merged branches. Branches older than this will be deleted. | No | `7` |
| `github_token` | Token with `repo` scope (automatically provided by `${{ secrets.GITHUB_TOKEN }}`). | Yes | N/A |

## Example Workflow

```yaml
name: Clean up stale merged branches
on:
  schedule:
    - cron: "0 3 * * *"  # runs daily at 03:00 UTC
jobs:
  branch-cleaner:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Delete stale merged branches
        uses: ./nightly-pr-branch-cleaner
        with:
          days_to_keep: 14
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## How It Works

1. Lists all branches in the repository.
2. For each branch, checks if it is merged into the default branch.
3. If merged and the last commit is older than `days_to_keep`, the branch is deleted.

The action is written in plain JavaScript and runs on `node20`.

## Testing

Run the tests locally with:

```bash
npm install
npm test
```

The test suite uses mocked GitHub API responses, so no network calls are made.
