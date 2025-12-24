# Nightly Ansible Playbook Validator

A whimsical-yet-useful utility for validating Ansible playbooks against syntax, idempotency, and best practices. Perfect for ensuring your infrastructure-as-code is battle-ready before deployment.

## Features

- **Syntax Validation**: Checks playbook syntax using `ansible-playbook --syntax-check`
- **Idempotency Testing**: Ensures playbooks can be run multiple times without side effects
- **Best Practices**: Validates against Ansible Lint rules
- **Molecule Integration**: Supports container-based testing with Molecule
- **Report Generation**: Creates detailed validation reports

## Usage

```bash
# Validate a single playbook
./validate_playbook.yml -i inventory.ini -p my_playbook.yml

# Validate all playbooks in a directory
./validate_playbook.yml -i inventory.ini -d playbooks/

# Generate validation report
./validate_playbook.yml -i inventory.ini -p my_playbook.yml --report
```

## Requirements

- Ansible 2.10+
- Molecule 3.0+
- Ansible Lint 5.0+
- Python 3.8+

## Installation

```bash
# Install dependencies
pip install molecule[lint] ansible-lint

# Clone and run
git clone <repo>
cd ansible-playbooks/nightly-ansible-playbook-validator
ansible-playbook validate_playbook.yml
```

## Output

The validator generates:
- Syntax validation results
- Idempotency test reports
- Best practice compliance scores
- Detailed remediation suggestions

## License

MIT
