# Nightly GitHub Actions Branch Cleaner

A reusable GitHub Action that automatically cleans up stale branches after PR merge/close, with configurable retention and safety filters.

## Features

- Automatically deletes branches after PR merge or close
- Configurable retention policies (time-based and count-based)
- Safety filters to protect important branches (main, master, production, etc.)
- Dry-run mode for safe testing
- Detailed logging and audit trail
- Works with any repository structure

## Usage

### Basic Usage

```yaml
name: Clean Stale Branches
on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Clean stale branches
        uses: polsala/ApocalypsAI/nightly-gha-branch-cleaner@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          dry-run: false
```

### Advanced Configuration

```yaml
name: Clean Stale Branches
on:
  pull_request:
    types: [closed]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Clean stale branches
        uses: polsala/ApocalypsAI/nightly-gha-branch-cleaner@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          protected-branches: 'main,master,production,staging,release/**'
          retention-days: 30
          max-branches-to-delete: 50
          dry-run: false
          verbose: true
```

## Inputs

| Input | Description | Default | Required |
|-------|-------------|---------|----------|
| `github-token` | GitHub token for API access | - | Yes |
| `protected-branches` | Comma-separated list of branch patterns to protect | `main,master` | No |
| `retention-days` | Delete branches older than this many days (0 = disabled) | `0` | No |
| `max-branches-to-delete` | Maximum number of branches to delete in one run | `100` | No |
| `dry-run` | Show what would be deleted without actually deleting | `true` | No |
| `verbose` | Enable verbose logging | `false` | No |

## Outputs

| Output | Description |
|--------|-------------|
| `deleted-branches` | JSON array of deleted branch names |
| `protected-branches` | JSON array of protected branch names that were skipped |
| `total-deleted` | Number of branches deleted |

## Examples

### Protect All Release Branches

```yaml
protected-branches: 'main,master,production,staging,release/**,hotfix/**'
```

### Weekly Cleanup with Count Limit

```yaml
retention-days: 7
max-branches-to-delete: 20
```

### Dry Run for Testing

```yaml
dry-run: true
verbose: true
```

## Safety Features

- **Protected Branch Patterns**: Uses glob patterns to protect critical branches
- **Rate Limiting**: Respects GitHub API rate limits
- **Dry Run Mode**: Test without making changes
- **Audit Logging**: Detailed logs of all operations
- **Batch Limits**: Prevents accidental mass deletions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT
