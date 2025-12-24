# Nightly Ephemeral Runner Orchestrator

A whimsical-yet-useful Bash utility that automates the lifecycle of ephemeral GitHub Actions runners. It provisions, monitors, and cleans up runners to ensure optimal performance and cost efficiency.

## Features

- **Provision Runners**: Spin up ephemeral runners on demand
- **Health Checks**: Monitor runner health and performance
- **Cleanup**: Automatically clean up idle or unhealthy runners
- **Logging**: Detailed logs for troubleshooting

## Usage

```bash
# Provision a new runner
./src/main.sh provision --token YOUR_GITHUB_TOKEN --org YOUR_ORG

# Check runner health
./src/main.sh health-check --org YOUR_ORG

# Cleanup idle runners
./src/main.sh cleanup --org YOUR_ORG

# Show help
./src/main.sh --help
```

## Requirements

- Bash 4.0+
- `curl` for API calls
- `jq` for JSON parsing
- GitHub Personal Access Token with `admin:org` scope

## Installation

1. Clone this utility
2. Make the script executable: `chmod +x src/main.sh`
3. Run with desired commands

## License

MIT
