# Nightly Git Branch Pruner

A GitHub Action that automatically closes stale branches based on configurable inactivity and naming rules.

## Features

- **Configurable inactivity threshold**: Set how many days of inactivity before a branch is considered stale
- **Protected branch patterns**: Define which branches should never be closed (supports wildcards)
- **Dry run mode**: Test the action before actually closing branches
- **Automatic PR creation**: Creates pull requests to close stale branches instead of force-deleting them
- **Comprehensive logging**: Detailed logs with timestamps and color coding

## Usage

### Basic Usage

```yaml
name: Nightly Branch Pruner

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM

jobs:
  prune-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Prune stale branches
        uses: polsala/ApocalypsAI/nightly-git-branch-pruner@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

### Advanced Configuration

```yaml
name: Nightly Branch Pruner

on:
  schedule:
    - cron: '0 2 * * *'

jobs:
  prune-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Prune stale branches
        uses: polsala/ApocalypsAI/nightly-git-branch-pruner@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          days-inactive: 14
          protected-branches: main,master,develop,dev,release/*,hotfix/*
          dry-run: false
```

## Inputs

| Input | Description | Default | Required |
|-------|-------------|---------|----------|
| `token` | GitHub token for API access | - | Yes |
| `days-inactive` | Number of days after which a branch is considered stale | `30` | No |
| `protected-branches` | Comma-separated list of branch patterns to protect from pruning | `main,master,develop,dev,release/*` | No |
| `dry-run` | Set to 'true' to perform a dry run without actually closing branches | `false` | No |

## Protected Branch Patterns

The action supports glob-style patterns for protected branches:

- `main` - Exact match for 'main'
- `release/*` - Matches 'release/v1.0', 'release/v2.0', etc.
- `feature/*` - Matches any branch starting with 'feature/'

## Dry Run Mode

When `dry-run` is set to `true`, the action will log what it would do without actually creating pull requests or making any changes. This is useful for testing your configuration.

## Example Workflow

```yaml
name: Nightly Maintenance

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:     # Manual trigger

jobs:
  nightly-tasks:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Prune stale branches
        uses: polsala/ApocalypsAI/nightly-git-branch-pruner@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          days-inactive: 7
          protected-branches: main,master,develop,dev,release/*,hotfix/*
          dry-run: false
```

## Security Considerations

- The action requires `GITHUB_TOKEN` with appropriate permissions to create pull requests
- Branches are closed via pull requests rather than force deletion to preserve history
- Protected branches are never modified, even in dry run mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## License

MIT
