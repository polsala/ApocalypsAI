# Nightly Ephemeral Runner Ghost Buster

Detects and cleans up orphaned ephemeral GitHub Actions runners across AWS, Azure, and GCP.

## Purpose

When using ephemeral runners, instances can sometimes be left behind due to:
- Workflow timeouts
- Provider API failures
- Unexpected shutdowns

This playbook identifies and terminates these orphaned instances to prevent cost leakage.

## Prerequisites

- Ansible 2.18+
- Cloud provider CLI credentials configured
- Python modules: boto3, azure-mgmt-compute, google-cloud-compute

## Usage

```bash
# Run the ghost buster
ansible-playbook ghost_buster.yml -i inventory.ini

# Run with debug output
ansible-playbook ghost_buster.yml -i inventory.ini -vvv

# Run specific provider cleanup
ansible-playbook ghost_buster.yml -i inventory.ini --tags aws
```

## Inventory

Create `inventory.ini` with your cloud provider details:

```ini
[aws]
aws-runner-1 ansible_host=1.2.3.4

[azure]
azure-runner-1 ansible_host=5.6.7.8

[gcp]
gcp-runner-1 ansible_host=9.10.11.12
```

## Output

The playbook generates a report showing:
- Detected orphaned instances
- Instances terminated
- Cost savings estimate

## Testing

```bash
# Run tests
ansible-playbook tests/test_ghost_buster.yml -i tests/test_inventory.ini
```

## License

MIT
