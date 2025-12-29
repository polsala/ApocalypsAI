# Nightly Ansible Playbook Validator

A whimsical-yet-useful utility that validates Ansible playbooks for syntax, idempotency, and security best practices. Perfect for ensuring your infrastructure-as-code is robust and secure!

## Features

- **Syntax Validation**: Checks YAML syntax and Ansible playbook structure
- **Idempotency Testing**: Verifies that playbooks can be run multiple times safely
- **Security Analysis**: Detects common security anti-patterns
- **Best Practices**: Enforces Ansible community best practices
- **Whimsical Reports**: Generates colorful, detailed validation reports

## Usage

```bash
# Validate a single playbook
ansible-playbook-validator validate playbook.yml

# Validate multiple playbooks
ansible-playbook-validator validate *.yml

# Generate a detailed report
ansible-playbook-validator validate --report detailed playbook.yml

# Check idempotency
ansible-playbook-validator idempotency playbook.yml

# Security audit
ansible-playbook-validator security playbook.yml
```

## Installation

```bash
# Clone the utility
git clone <repository>
cd ansible-playbooks/nightly-ansible-playbook-validator

# Install dependencies
pip install -r requirements.txt

# Run the validator
python src/validator.py --help
```

## Output

The validator provides:
- **Syntax Check**: Pass/Fail with line numbers for errors
- **Idempotency Score**: Percentage of tasks that are idempotent
- **Security Score**: Risk assessment with specific recommendations
- **Best Practices Score**: Compliance with community standards
- **Detailed Report**: Comprehensive analysis with suggestions

## Examples

### Basic Validation
```bash
$ ansible-playbook-validator validate webserver.yml

✓ Syntax: Valid YAML and Ansible structure
✓ Idempotency: 85% of tasks are idempotent
✓ Security: No critical issues detected
✓ Best Practices: Following 90% of recommended patterns

Overall Score: 88.75/100
```

### Security Audit
```bash
$ ansible-playbook-validator security webserver.yml

Security Analysis Report:
- Passwords: ✓ No plaintext passwords detected
- Privilege Escalation: ⚠️  Some tasks use become: true without explicit justification
- File Permissions: ✓ Proper permissions set
- Network Security: ✓ No open ports detected

Recommendations:
1. Add comments explaining why privilege escalation is needed
2. Consider using vault for sensitive variables
```

## Integration

This validator can be integrated into CI/CD pipelines to automatically validate Ansible playbooks before deployment.

```yaml
# GitHub Actions example
- name: Validate Ansible Playbooks
  run: |
    cd ansible-playbooks/nightly-ansible-playbook-validator
    python src/validator.py validate ../path/to/playbooks/*.yml
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Support

For issues and questions, please open a GitHub issue or join our community discussions.
