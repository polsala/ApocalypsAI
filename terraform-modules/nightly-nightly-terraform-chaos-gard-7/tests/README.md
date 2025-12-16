# Chaos Garden Orchestrator Tests

This directory contains tests for the Terraform Chaos Garden Orchestrator module.

## Test Files

- `terraform-validator.sh` - Shell script to validate Terraform configuration

## Running Tests

### Prerequisites

- Terraform (>= 1.0)
- Bash
- jq (for JSON parsing)

### Execute Tests

```bash
# Make the script executable
chmod +x tests/terraform-validator.sh

# Run the validation
./tests/terraform-validator.sh
```

## Test Coverage

The test suite validates:

1. **Terraform Installation** - Checks Terraform is installed and accessible
2. **Required Files** - Verifies all required Terraform files exist
3. **Configuration Validation** - Runs `terraform init` and `terraform validate`
4. **Examples** - Validates example configurations
5. **Modules** - Checks for required modules and components
6. **Variable Validation** - Ensures proper variable validation is in place
7. **Security** - Checks for security best practices
8. **Report Generation** - Creates a comprehensive validation report

## Expected Output

If all tests pass, you should see:

```
[2024-01-01 12:00:00] Starting Terraform validation for Chaos Garden Orchestrator
[2024-01-01 12:00:00] Terraform version: 1.6.0
[2024-01-01 12:00:00] Checking for required files...
[2024-01-01 12:00:00] All required files present!
[2024-01-01 12:00:00] Validating Terraform configuration...
[2024-01-01 12:00:00] Terraform configuration is valid!
[2024-01-01 12:00:00] Examples directory found
[2024-01-01 12:00:00] Basic example found
[2024-01-01 12:00:00] Basic example is valid!
[2024-01-01 12:00:00] Modules directory found
[2024-01-01 12:00:00] Chaos container module found
[2024-01-01 12:00:00] Chaos container Dockerfile found
[2024-01-01 12:00:00] Chaos scripts directory found
[2024-01-01 12:00:00] Failure rate validation found
[2024-01-01 12:00:00] Whimsy level validation found
[2024-01-01 12:00:00] Sensitive variables found
[2024-01-01 12:00:00] No hardcoded secrets detected
[2024-01-01 12:00:00] Generating validation report...
[2024-01-01 12:00:00] Validation report saved to: /path/to/validation-report.md
[2024-01-01 12:00:00] Terraform validation completed successfully!
```

## Validation Report

After running the tests, a `validation-report.md` file will be generated in the root directory with detailed information about:

- Terraform version used
- Configuration status
- Files checked
- Examples status
- Modules status
- Security checks
- Variable validation status

## Troubleshooting

### Terraform Not Found

If you get an error about Terraform not being found:

```bash
ERROR: Terraform is not installed. Please install Terraform first.
```

Install Terraform following the [official installation guide](https://developer.hashicorp.com/terraform/install).

### Validation Failures

If Terraform validation fails, check:

1. All required files are present
2. Terraform syntax is correct
3. Required variables are provided
4. Provider configuration is correct

### Missing jq

If you get errors about jq:

```bash
# On macOS
brew install jq

# On Ubuntu/Debian
sudo apt-get install jq

# On CentOS/RHEL
sudo yum install jq
```

## Continuous Integration

This test suite can be integrated into CI/CD pipelines to automatically validate Terraform configurations before deployment.

Example GitHub Actions workflow:

```yaml
name: Terraform Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0
      - name: Install jq
        run: sudo apt-get install -y jq
      - name: Run validation tests
        run: ./tests/terraform-validator.sh
```

---

*For more information about the Chaos Garden Orchestrator, see the main README.md.*
