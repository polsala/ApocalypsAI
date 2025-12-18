# Tests for Terraform Chaos Monkey

This directory contains automated tests for the chaos monkey module.

## Test Files

- `terraform_validate.sh` - Validates Terraform syntax and configuration
- `chaos_simulation_test.sh` - Simulates different chaos scenarios
- `README.md` - This documentation file

## Running Tests

```bash
# Make test scripts executable
chmod +x tests/*.sh

# Run validation tests
./tests/terraform_validate.sh

# Run simulation tests
./tests/chaos_simulation_test.sh
```

## Test Coverage

- Terraform syntax validation
- Safe mode functionality
- Different intensity levels
- Enabled/disabled states
- Multiple cloud provider configurations
