# Chaos Monkey Module Tests

This directory contains tests for the Terraform Chaos Monkey module.

## Test Structure

- `test_basic.tf` - Basic functionality tests
- `test_integration.tf` - Integration tests with real resources
- `test_security.tf` - Security and safety tests

## Running Tests

### Prerequisites

1. Install Terraform >= 1.0
2. Configure AWS credentials (for integration tests)
3. Install required providers

### Test Commands

```bash
# Initialize test environment
terraform init

# Validate configuration
terraform validate

# Plan test execution
terraform plan -var-file="test.tfvars"

# Apply test configuration
terraform apply -var-file="test.tfvars" -auto-approve

# Destroy test resources
terraform destroy -var-file="test.tfvars" -auto-approve
```

### Test Variables

Create a `test.tfvars` file with your test configuration:

```hcl
# Test configuration
aws_region = "us-east-1"

# Chaos Monkey settings
chaos_enabled     = true
chaos_probability = 0.1
dry_run          = true
```

## Test Scenarios

### Basic Functionality Tests

1. **Module Initialization** - Verify module can be initialized
2. **Variable Validation** - Test all input variables
3. **Output Generation** - Verify all outputs are generated correctly

### Integration Tests

1. **Resource Targeting** - Test resource selection logic
2. **Chaos Execution** - Verify chaos execution in dry-run mode
3. **Metrics Collection** - Test metrics generation and output

### Security Tests

1. **Safety Validation** - Verify safety checks work correctly
2. **Exclusion Logic** - Test resource exclusion functionality
3. **Dry-run Protection** - Verify dry-run mode prevents actual destruction

## Test Coverage

- [x] Module initialization
- [x] Variable validation
- [x] Output generation
- [x] Safety checks
- [x] Dry-run functionality
- [ ] Integration with real AWS resources
- [ ] Performance under load
- [ ] Error handling

## Continuous Integration

These tests should be run in CI/CD pipeline:

1. `terraform validate` - Validate syntax and structure
2. `terraform plan` - Test planning phase
3. `terraform apply` - Test application (in test environment)
4. `terraform destroy` - Clean up test resources

## Troubleshooting

### Common Issues

1. **Provider errors** - Ensure AWS provider is configured correctly
2. **Permission errors** - Check IAM permissions for test account
3. **State conflicts** - Use unique workspace names for parallel tests

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
export TF_LOG=DEBUG
terraform plan
```

### Test Isolation

Each test run should use a unique workspace to avoid conflicts:

```bash
terraform workspace new test-$(date +%s)
```

## Contributing Tests

When adding new tests:

1. Follow the existing naming convention
2. Add appropriate comments and documentation
3. Ensure tests are self-contained
4. Update this README with new test scenarios
5. Verify tests pass in CI/CD pipeline
