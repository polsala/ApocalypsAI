# Nightly Ansible Playbook Validator

A robust validation suite for Ansible playbooks that ensures syntax correctness, idempotency, and adherence to best practices.

## Features

- **Syntax Validation**: Checks playbook syntax using Ansible's built-in parser
- **Idempotency Testing**: Ensures playbooks can be run multiple times without side effects
- **Best Practices**: Validates against Ansible Lint rules and community standards
- **Molecule Integration**: Uses Molecule for comprehensive testing scenarios
- **Report Generation**: Creates detailed validation reports with actionable feedback

## Usage

### Prerequisites

```bash
# Install required tools
pip install ansible molecule ansible-lint
```

### Basic Validation

```bash
# Run validation on a playbook
ansible-playbook -i inventory validate_playbook.yml
```

### Molecule Testing

```bash
# Navigate to playbook directory
cd path/to/playbook

# Run molecule tests
molecule test
```

### Generate Report

```bash
# Generate validation report
ansible-playbook -i inventory validate_playbook.yml --extra-vars "generate_report=true"
```

## Configuration

### Inventory Setup

Create an `inventory.ini` file:

```ini
[all]
localhost ansible_connection=local
```

### Variables

Create a `vars/main.yml` file with validation settings:

```yaml
validation_settings:
  strict_mode: true
  check_idempotency: true
  generate_report: true
  report_format: "html"
```

## Testing

### Unit Tests

```bash
# Run unit tests
python -m pytest tests/test_validator.py -v
```

### Integration Tests

```bash
# Run integration tests
molecule test --all
```

## Report Output

Validation reports are generated in the `reports/` directory with:

- **Syntax Check Results**: Detailed syntax validation output
- **Idempotency Test Results**: Before/after state comparisons
- **Best Practice Violations**: Lint rule violations with suggestions
- **Overall Score**: Composite validation score

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
