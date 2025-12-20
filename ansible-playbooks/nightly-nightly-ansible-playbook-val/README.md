# Nightly Ansible Playbook Validator

A whimsical-yet-powerful utility that validates Ansible playbooks for syntax, idempotency, and best practices. Think of it as your friendly neighborhood playbook inspector with a sense of humor!

## Features

- **Syntax Validation**: Checks YAML syntax and Ansible structure
- **Idempotency Testing**: Ensures playbooks can run multiple times safely
- **Best Practices**: Validates against common Ansible anti-patterns
- **Multi-Stage Pipeline**: Runs validation in progressive stages
- **Colorful Reports**: Generates human-readable validation reports

## Usage

```bash
# Validate a single playbook
ansible-playbook-validator validate playbook.yml

# Validate multiple playbooks
ansible-playbook-validator validate *.yml

# Generate validation report
ansible-playbook-validator report --output validation_report.html

# Check idempotency
ansible-playbook-validator idempotency test_playbook.yml
```

## Installation

```bash
# Clone the validator
git clone <repository>
cd ansible-playbook-validator

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x validate_playbooks.py
```

## Requirements

- Python 3.8+
- Ansible
- PyYAML
- Jinja2
- rich (for pretty output)

## Output

The validator provides:
- ✅ Syntax validation results
- 🔄 Idempotency test outcomes
- 📋 Best practices compliance
- 🎨 Colorful, easy-to-read reports

## License

MIT License - because validation should be free and open!
