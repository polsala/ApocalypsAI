# Nightly Ansible Playbook Validator

A whimsical-yet-useful utility for validating Ansible playbooks against syntax, idempotency, and security best practices.

## Features

- **Syntax Validation**: Checks YAML syntax and Ansible playbook structure
- **Idempotency Testing**: Verifies playbooks can be run multiple times safely
- **Security Analysis**: Detects common security anti-patterns
- **Best Practices**: Enforces Ansible community standards
- **Report Generation**: Creates detailed validation reports

## Usage

```bash
# Validate a single playbook
ansible-playbook-validator validate playbook.yml

# Validate multiple playbooks
ansible-playbook-validator validate --path ./playbooks/

# Generate detailed report
ansible-playbook-validator validate --report report.html playbook.yml

# Check idempotency
ansible-playbook-validator idempotency test-playbook.yml

# Security audit
ansible-playbook-validator security audit playbook.yml
```

## Installation

```bash
# Clone the utility
git clone <repository-url>
cd ansible-playbooks/nightly-ansible-playbook-validator

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x src/validator.py
```

## Requirements

- Python 3.8+
- Ansible
- PyYAML
- Jinja2

## Output

The validator provides:

- **Summary Report**: Overall validation status
- **Detailed Findings**: Specific issues with line numbers
- **Security Score**: Risk assessment (0-100)
- **Recommendations**: Actionable improvement suggestions

## Examples

See the `examples/` directory for sample playbooks and validation reports.

## Contributing

Contributions welcome! Please:

1. Add tests for new validation rules
2. Update documentation
3. Follow the existing code style

## License

MIT License
