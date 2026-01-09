# Nightly Ansible Playbook Linter

A static analysis and linting tool for Ansible playbooks that performs YAML validation, syntax checks, and best practice enforcement.

## Features

- **YAML Validation**: Ensures playbooks are valid YAML
- **Syntax Checking**: Validates Ansible-specific syntax
- **Best Practice Enforcement**: Checks for common anti-patterns
- **Security Analysis**: Identifies potential security issues
- **Performance Checks**: Flags performance bottlenecks
- **Multi-File Support**: Analyzes entire playbook directories

## Usage

```bash
# Lint a single playbook
ansible-playbook-linter playbook.yml

# Lint an entire directory
ansible-playbook-linter --recursive playbooks/

# Generate detailed report
ansible-playbook-linter --report report.json playbooks/

# Check specific rules only
ansible-playbook-linter --rules syntax,security playbook.yml
```

## Installation

```bash
# Clone the utility
git clone <repository>
cd ansible-playbook-linter

# Run directly (no dependencies)
python3 src/linter.py --help
```

## Output Format

The linter outputs structured JSON with:

- **Summary**: Overall statistics
- **Violations**: Detailed rule violations with line numbers
- **Suggestions**: Actionable recommendations
- **Security Issues**: Potential security concerns

## Rules

### Syntax Rules
- `yaml-valid`: Ensures valid YAML syntax
- `task-name-required`: All tasks must have names
- `module-exists`: Validates module names

### Security Rules
- `no-hardcoded-secrets`: Detects potential secrets
- `sudo-usage`: Warns about sudo usage
- `file-permissions`: Checks file permission settings

### Performance Rules
- `loop-optimization`: Suggests loop optimizations
- `gather-facts`: Checks gather_facts usage

### Best Practice Rules
- `variable-naming`: Enforces consistent naming
- `handler-usage`: Validates handler patterns

## Configuration

Create `.ansible-lint.yml` in your project root:

```yaml
rules:
  enabled:
    - yaml-valid
    - task-name-required
    - no-hardcoded-secrets
  disabled:
    - loop-optimization

exclude:
  - vendor/
  - tests/fixtures/
```

## CI/CD Integration

```yaml
# .github/workflows/lint.yml
name: Ansible Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Ansible Linter
        run: |
          python3 utils/nightly-ansible-playbook-linter/src/linter.py --report lint-results.json playbooks/
          python3 utils/nightly-ansible-playbook-linter/src/reporter.py lint-results.json
```

## Exit Codes

- `0`: No violations found
- `1`: Violations found
- `2`: Configuration error
- `3`: File not found
- `4`: YAML parsing error

## Examples

### Basic Usage

```bash
# Check a single file
ansible-playbook-linter web-server.yml

# Check multiple files
ansible-playbook-linter web-server.yml db-server.yml

# Recursive directory check
ansible-playbook-linter --recursive infrastructure/
```

### Advanced Usage

```bash
# Generate JSON report
ansible-playbook-linter --report results.json --format json playbooks/

# Custom configuration
ansible-playbook-linter --config .ansible-lint.yml playbooks/

# Verbose output
ansible-playbook-linter --verbose playbooks/
```

## Contributing

1. Fork the repository
2. Add new rules to `rules/` directory
3. Update tests in `tests/`
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
