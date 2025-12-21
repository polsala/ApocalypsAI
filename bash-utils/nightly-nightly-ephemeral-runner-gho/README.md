# Nightly Ephemeral Runner Ghost Buster

A shell script that detects and cleans up orphaned ephemeral GitHub Actions runners across multiple repositories.

## Purpose

When using ephemeral runners, sometimes runners can become orphaned due to:
- Network issues during registration
- Unexpected shutdowns
- Failed cleanup operations
- Repository migrations

This utility helps identify and remove these ghost runners to keep your runner pools clean.

## Features

- Scans multiple repositories for registered runners
- Identifies orphaned runners (registered but not currently active)
- Provides dry-run mode for safe testing
- Generates cleanup reports
- Supports GitHub Enterprise Server and GitHub.com
- Configurable retention policies

## Requirements

- `curl` (for API calls)
- `jq` (for JSON parsing)
- GitHub personal access token with `repo` scope
- Bash 4.0+

## Usage

### Basic Usage

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_personal_access_token"

# Run with default settings
./src/ghost_buster.sh

# Run with dry-run mode (recommended first run)
./src/ghost_buster.sh --dry-run
```

### Advanced Usage

```bash
# Specify repositories to scan
./src/ghost_buster.sh --repos "owner/repo1,owner/repo2"

# Set custom retention period (days)
./src/ghost_buster.sh --retention-days 7

# Output to file
./src/ghost_buster.sh --output report.json

# Enable verbose logging
./src/ghost_buster.sh --verbose
```

### Configuration File

Create a `config.json` file for persistent settings:

```json
{
  "github_token": "your_token",
  "api_base_url": "https://api.github.com",
  "repositories": [
    "owner/repo1",
    "owner/repo2"
  ],
  "retention_days": 3,
  "dry_run": false,
  "verbose": true
}
```

## Command Line Options

- `--repos <list>`: Comma-separated list of repositories to scan
- `--retention-days <days>`: Keep runners registered within this many days
- `--dry-run`: Show what would be deleted without actually deleting
- `--output <file>`: Write report to specified file
- `--verbose`: Enable detailed logging
- `--help`: Show help message

## Environment Variables

- `GITHUB_TOKEN`: Personal access token for GitHub API
- `GITHUB_API_URL`: Custom API base URL (for GitHub Enterprise)

## Output

The script generates a JSON report with:

- Summary of findings
- List of orphaned runners
- Actions taken
- Any errors encountered

## Safety Features

- Dry-run mode for testing
- Configurable retention policies
- Detailed logging
- Error handling with rollback
- Confirmation prompts for destructive operations

## Integration with CI/CD

Add to your GitHub Actions workflow:

```yaml
name: Ghost Buster
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Ghost Buster
        run: |
          export GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
          ./src/ghost_buster.sh --dry-run
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
