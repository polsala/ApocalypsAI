# Nightly Ephemeral Runner Harvester

A whimsical-yet-useful Bash utility that harvests and reuses ephemeral GitHub self-hosted runners across multiple repositories. Perfect for CI/CD teams looking to optimize runner usage and reduce costs.

## Features

- **Harvest Runners**: Automatically discovers and registers ephemeral runners from multiple repositories
- **Reuse Runners**: Reuses existing runners to minimize resource consumption
- **Cost Optimization**: Tracks runner usage and provides cost-saving recommendations
- **Multi-Repo Support**: Works across multiple GitHub repositories
- **Self-Healing**: Automatically handles runner failures and re-registration

## Requirements

- Bash 4.0+
- GitHub CLI (`gh`) installed and authenticated
- jq for JSON parsing
- curl for API requests

## Installation

```bash
# Clone or copy the script to your system
chmod +x harvest_runners.sh
```

## Usage

### Basic Harvest

```bash
# Harvest runners from all configured repositories
./harvest_runners.sh --harvest
```

### Reuse Existing Runners

```bash
# Reuse existing runners across repositories
./harvest_runners.sh --reuse
```

### Cost Analysis

```bash
# Generate cost optimization report
./harvest_runners.sh --cost-analysis
```

### Full Workflow

```bash
# Complete workflow: harvest, reuse, and analyze
./harvest_runners.sh --full
```

## Configuration

Create a `.runner-config` file in your working directory:

```yaml
# .runner-config
repositories:
  - owner/repo1
  - owner/repo2
  - owner/repo3
runner_labels:
  - "ephemeral"
  - "cost-optimized"
max_runners_per_repo: 5
harvest_interval: 300  # seconds
```

## Command Line Options

- `--harvest`: Discover and register new runners
- `--reuse`: Reuse existing runners across repositories
- `--cost-analysis`: Generate cost optimization report
- `--full`: Run complete workflow (harvest + reuse + analysis)
- `--config <file>`: Specify configuration file path
- `--verbose`: Enable verbose logging
- `--help`: Show help message

## Output

The utility generates:

- **Harvest Report**: List of discovered and registered runners
- **Reuse Report**: Summary of runner reuse across repositories
- **Cost Report**: Cost optimization recommendations and savings
- **Logs**: Detailed operation logs for debugging

## Examples

### Harvest from Specific Repositories

```bash
./harvest_runners.sh --harvest --config custom-config.yaml
```

### Reuse with Verbose Logging

```bash
./harvest_runners.sh --reuse --verbose
```

### Generate Cost Analysis Only

```bash
./harvest_runners.sh --cost-analysis
```

## Safety Features

- **Rate Limiting**: Respects GitHub API rate limits
- **Error Handling**: Graceful handling of API failures
- **Dry Run Mode**: Preview changes before applying
- **Backup**: Creates backup of runner configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please:
1. Check the logs for error details
2. Verify your GitHub CLI authentication
3. Ensure you have the required permissions for target repositories
4. Open an issue with detailed reproduction steps
