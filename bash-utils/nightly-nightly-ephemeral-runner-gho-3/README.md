# Nightly Ephemeral Runner Ghost Buster

A lightweight Bash utility that detects and cleans up orphaned GitHub Actions runners across AWS, Azure, and GCP. Perfect for maintaining clean infrastructure when using ephemeral runners.

## Features

- Detects orphaned runners across multiple cloud providers
- Generates detailed cleanup reports
- Supports dry-run mode for safe testing
- Configurable age thresholds for cleanup
- Minimal dependencies - just Bash and cloud CLI tools

## Usage

```bash
# Dry run to see what would be cleaned up
./ghost_buster.sh --dry-run --age 2h

# Actually clean up runners older than 2 hours
./ghost_buster.sh --age 2h

# Clean up across specific providers only
./ghost_buster.sh --providers aws,azure --age 1h
```

## Installation

```bash
# Clone or download the script
chmod +x ghost_buster.sh

# Install required cloud CLI tools
# AWS: aws-cli
# Azure: az-cli
# GCP: gcloud
```

## Configuration

Set environment variables for cloud authentication:

```bash
export AWS_PROFILE=your-profile
export AZURE_SUBSCRIPTION_ID=your-subscription
export GOOGLE_APPLICATION_CREDENTIALS=path/to/creds.json
```

## Requirements

- Bash 4.0+
- AWS CLI (for AWS detection)
- Azure CLI (for Azure detection)
- Google Cloud SDK (for GCP detection)
- jq (for JSON parsing)

## Safety Features

- Dry-run mode shows what would be deleted without making changes
- Configurable age thresholds prevent accidental cleanup of active runners
- Detailed logging for audit trails
- Provider-specific error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with dry-run mode
4. Submit a pull request

## License

MIT
