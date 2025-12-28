# Nightly Ansible Ephemeral Runner Orchestrator

Automates the lifecycle of ephemeral GitHub Actions runners across multiple cloud providers with health checks, scaling, and cleanup.

## Features

- **Multi-cloud support**: AWS EC2, Azure VM, GCP Compute Engine
- **Auto-scaling**: Scale runners based on queue length
- **Health monitoring**: Continuous health checks with automatic recovery
- **Ephemeral lifecycle**: Automatic cleanup after job completion or timeout
- **Security**: Temporary credentials and network isolation
- **Reporting**: Detailed logs and metrics

## Quick Start

### Prerequisites

- Ansible 2.14+
- Cloud provider CLI configured
- GitHub Actions runner token

### Installation

```bash
# Clone or copy the playbook
ansible-playbook -i inventory.ini provision_runners.yml -e "github_token=your_token"
```

### Configuration

Edit `vars/main.yml` to configure:
- Cloud provider settings
- Instance types and regions
- Scaling thresholds
- Health check intervals

## Usage

### Provision Runners

```bash
ansible-playbook -i inventory.ini provision_runners.yml
```

### Health Check

```bash
ansible-playbook -i inventory.ini health_check.yml
```

### Cleanup Orphans

```bash
ansible-playbook -i inventory.ini cleanup_runners.yml
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub API    │    │   Ansible       │    │   Cloud Provider│
│   (Queue Check) │───▶│   (Orchestrator)│───▶│   (EC2/Azure/GCP)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Health Check  │    │   Runner Cleanup│
                       │   (Monitoring)  │    │   (Orphaned VMs)│
                       └─────────────────┘    └─────────────────┘
```

## Variables

See `vars/main.yml` for all configurable options:

- `cloud_provider`: aws|azure|gcp
- `instance_type`: VM size
- `region`: Cloud region
- `max_runners`: Maximum concurrent runners
- `health_check_interval`: Seconds between checks
- `cleanup_timeout`: Hours before force cleanup

## Monitoring

The orchestrator provides:

- **Queue monitoring**: GitHub Actions queue length
- **Runner health**: Registration status and job completion
- **Resource usage**: CPU, memory, and network metrics
- **Cost tracking**: Instance uptime and billing estimates

## Security

- Uses temporary IAM roles/credentials
- Network isolation with security groups
- Encrypted communication
- Automatic credential rotation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test with multiple cloud providers
4. Submit a pull request

## License

MIT - see LICENSE file for details.
