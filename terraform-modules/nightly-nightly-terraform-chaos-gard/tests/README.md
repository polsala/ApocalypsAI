# Chaos Garden Tests

This directory contains tests for the Terraform Chaos Garden module.

## Test Structure

- **test_basic.tf**: Basic integration tests covering different chaos levels
- **test_validation.sh**: Shell script to validate the module configuration
- **test_outputs.tf**: Additional output validation tests

## Running Tests

### Prerequisites

- Terraform 1.0+
- Python 3.6+ (for validation scripts)

### Test Commands

```bash
# Initialize the test directory
terraform init

# Validate the configuration
terraform validate

# Plan the test deployment (dry run)
terraform plan -var-file="test_vars.tfvars"

# Run validation script
./tests/test_validation.sh
```

## Test Scenarios

1. **Disabled Chaos Garden** (chaos_level = 0, enabled = false)
   - Expected: Chaos status shows "DISABLED"
   - Expected: No chaos events triggered

2. **Low Chaos Level** (chaos_level = 2)
   - Expected: Chaos status shows "ACTIVE"
   - Expected: Severity is "Moderate"
   - Expected: Protected resources are configured

3. **High Chaos Level** (chaos_level = 7)
   - Expected: Chaos status shows "ACTIVE"
   - Expected: Severity is "Severe"
   - Expected: Schedule is configured

## Validation Criteria

- Chaos level must be between 0 and 10
- Protected resources list must be valid
- Outputs must match expected values
- No sensitive data should be exposed in non-sensitive outputs

## Safety Notes

- These tests use the `null_resource` provider for demonstration
- In real environments, chaos events would use cloud-specific providers
- Always test in non-production environments first

## Troubleshooting

If tests fail:

1. Check Terraform version compatibility
2. Verify all required variables are set
3. Ensure no syntax errors in configuration
4. Review validation error messages

## Test Data

Test variables are defined in `test_vars.tfvars` (not included in this example).

Example test_vars.tfvars:
```hcl
# Test configuration
chaos_level = 3
enabled = true
protected_resources = ["test-resource"]
chaos_schedule = "0 2 * * *"
```
