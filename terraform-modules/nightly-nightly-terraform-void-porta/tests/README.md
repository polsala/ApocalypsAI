# Void Portal Module Tests

This directory contains test cases for the nightly-terraform-void-portal module.

## Test Structure

- `test_void_portal.tf` - Main test configuration with multiple test scenarios

## Test Scenarios

1. **Basic Portal Creation**
   - Creates a simple portal with minimal configuration
   - Tests: portal ID generation, basic outputs

2. **Tracked Portal**
   - Enables resource tracking and cleanup
   - Tests: tracking functionality, cleanup schedule generation

3. **Multi-Provider Portal**
   - Tests with multiple cloud providers
   - Tests: provider list handling, resource inventory

4. **Debug Portal**
   - Enables debug mode and custom severity
   - Tests: debug configuration, metadata output

## Running Tests

```bash
# Initialize the test directory
terraform init

# Validate configuration
terraform validate

# Plan the test resources
terraform plan -var-file="test.tfvars"

# Apply test resources
terraform apply -var-file="test.tfvars"

# Destroy test resources
terraform destroy -var-file="test.tfvars"
```

## Test Variables

Create a `test.tfvars` file with:

```hcl
# Test configuration can be customized here
# Most tests use default values from the module
```

## Expected Results

- All portal IDs should be 32-character hex strings
- Portal names should follow the pattern: `{portal_name}-{pet_name}-{random_string}`
- Tracked resources should contain entries for all specified providers
- Cleanup schedule should be a valid cron expression when enabled
- Portal status should reflect the configuration settings

## Validation Tests

The module includes validation rules that should be tested:

- Empty providers list should cause validation error
- Invalid severity levels should cause validation error
- Negative auto_cleanup_days should cause validation error

These are automatically tested by `terraform validate`.
