# Nightly Ephemeral Runner Harvester

Harvests and reuses idle ephemeral GitHub Actions runners across repositories to maximize CI throughput.

## Overview

When ephemeral runners are provisioned on demand, they often sit idle after completing a job. This utility identifies idle runners and reuses them for subsequent jobs, reducing provisioning latency and resource waste.

## Features

- Detects idle ephemeral runners across multiple repositories
- Reuses idle runners for new jobs
- Logs harvesting activity for audit trails
- Supports dry-run mode for safe testing

## Usage

```bash
# Harvest idle runners (dry-run)
./src/harvest_runners.sh --dry-run

# Harvest idle runners (live)
./src/harvest_runners.sh

# Harvest with custom GitHub token
GITHUB_TOKEN=your_token ./src/harvest_runners.sh
```

## Requirements

- Bash 4.0+
- curl
- jq
- GitHub personal access token with repo scope

## Installation

1. Clone or copy the `src/harvest_runners.sh` script
2. Make it executable: `chmod +x src/harvest_runners.sh`
3. Set `GITHUB_TOKEN` environment variable or pass via `--token`

## Configuration

Set the following environment variables:

- `GITHUB_TOKEN`: GitHub personal access token
- `GITHUB_ORG`: GitHub organization name (optional, for org-wide harvesting)

## License

MIT
