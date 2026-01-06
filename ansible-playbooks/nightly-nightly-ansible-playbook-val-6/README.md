# Nightly Ansible Playbook Validator

A whimsical-yet-useful utility that validates Ansible playbooks for syntax, idempotency, and best practices. Perfect for ensuring your infrastructure-as-code is battle-ready!

## Features

- **Syntax Validation**: Checks playbook syntax using `ansible-playbook --syntax-check`
- **Idempotency Testing**: Ensures playbooks are truly idempotent using Molecule
- **Best Practices**: Lints playbooks with Ansible Lint
- **Multi-Provider Support**: Works with AWS, Azure, GCP, and local Docker
- **Report Generation**: Creates detailed validation reports

## Usage

```bash
# Validate a single playbook
cd ansible-playbooks/nightly-ansible-playbook-validator
ansible-playbook validate_playbooks.yml -e "playbook_path=/path/to/your/playbook.yml"

# Validate all playbooks in a directory
ansible-playbook validate_playbooks.yml -e "playbook_dir=/path/to/playbooks"

# Run with specific providers
ansible-playbook validate_playbooks.yml -e "providers=['docker', 'aws']"

# Generate report
ansible-playbook validate_playbooks.yml -e "generate_report=true"
```

## Requirements

- Ansible 2.12+
- Molecule 4.0+
- Ansible Lint 6.0+
- Docker (for local testing)
- Cloud provider CLI tools (for cloud testing)

## Installation

```bash
# Install requirements
pip install molecule[lint] ansible-lint

# Install cloud provider dependencies
pip install molecule[docker] molecule[aws] molecule[azure] molecule[gcp]
```

## Configuration

Edit `vars/main.yml` to customize validation settings:

```yaml
validation_settings:
  max_playbook_size: 1000  # lines
  allowed_modules:
    - apt
    - yum
    - dnf
    - service
    - file
    - template
    - copy
  forbidden_patterns:
    - "always_run"
    - "force=yes"
    - "ignore_errors: true"
```

## Output

The validator generates:

- **Validation Report**: `reports/validation_report.html`
- **JSON Summary**: `reports/validation_summary.json`
- **Detailed Logs**: `logs/validation.log`

## License

MIT License - see LICENSE file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Support

For issues and questions, please open a GitHub issue.
