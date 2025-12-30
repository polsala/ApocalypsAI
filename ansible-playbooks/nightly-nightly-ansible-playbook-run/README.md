# Nightly Ansible Playbook Runner

A whimsical-yet-useful utility for running and testing Ansible playbooks with automated validation and reporting.

## Features

- **Playbook Validation**: Syntax and structure validation before execution
- **Dry Run Mode**: Preview changes without making them
- **Multi-Environment Testing**: Test playbooks across different environments
- **Report Generation**: Detailed execution reports with success/failure metrics
- **Rollback Support**: Automatic rollback on failed deployments
- **Inventory Management**: Dynamic inventory validation and updates

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ansible-playbooks/nightly-ansible-playbook-runner

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Playbook Execution

```bash
# Run a playbook with validation
python runner.py --playbook site.yml --inventory production.ini

# Dry run mode
python runner.py --playbook site.yml --inventory production.ini --dry-run

# Multi-environment testing
python runner.py --playbook site.yml --environments dev,test,prod
```

### Advanced Options

```bash
# Enable rollback on failure
python runner.py --playbook site.yml --inventory production.ini --enable-rollback

# Generate detailed report
python runner.py --playbook site.yml --inventory production.ini --report-format html

# Custom timeout
python runner.py --playbook site.yml --inventory production.ini --timeout 300
```

## Configuration

Create a `config.yml` file to customize behavior:

```yaml
runner:
  default_timeout: 600
  enable_rollback: true
  report_format: html
  log_level: INFO

validation:
  check_syntax: true
  check_idempotency: true
  check_dependencies: true

environments:
  dev:
    inventory: inventories/dev.ini
    tags: ["development"]
  test:
    inventory: inventories/test.ini
    tags: ["testing"]
  prod:
    inventory: inventories/prod.ini
    tags: ["production"]
```

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/

# Test specific playbook
python runner.py --playbook tests/playbooks/test-playbook.yml --inventory tests/inventory.ini
```

## Report Formats

- **JSON**: Machine-readable execution data
- **HTML**: Human-readable detailed reports
- **Markdown**: Simple text-based reports
- **XML**: JUnit-compatible test results

## Rollback Strategy

The runner implements a smart rollback mechanism:

1. **Pre-execution Snapshot**: Capture current state
2. **Change Tracking**: Monitor all modifications
3. **Failure Detection**: Identify failed tasks
4. **Automatic Rollback**: Revert changes if failures occur
5. **Manual Rollback**: Manual rollback option for partial failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please:
- Check the [FAQ](docs/FAQ.md)
- Open an [issue](../../issues)
- Join our [Discord](https://discord.gg/example)

---

*May your playbooks always converge and your inventories never drift!*
