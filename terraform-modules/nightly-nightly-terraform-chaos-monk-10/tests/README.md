# Chaos Monkey Module Tests

This directory contains tests for the Terraform Chaos Monkey module.

## Test Structure

- `test_basic.tf` - Basic functionality and validation tests
- `test_integration.tf` - Integration tests with mock resources
- `test_security.tf` - Security and safety validation tests

## Running Tests

### Prerequisites

1. Install Terraform >= 1.0
2. Ensure you have appropriate AWS credentials (for integration tests)

### Test Commands

```bash
# Run basic validation tests
terraform init
terraform validate

# Run plan to see what would be created/destroyed
terraform plan -var-file="test-variables.tfvars"

# Apply the test configuration
terraform apply -var-file="test-variables.tfvars"

# Destroy test resources
terraform destroy -var-file="test-variables.tfvars"
```

### Test Variables

Create a `test-variables.tfvars` file:

```hcl
# Test environment settings
environment = "test"

# Enable chaos for testing
enable_chaos = true

# Test-specific configurations
chaos_schedule = "always"
dry_run = true
```

## Test Categories

### 1. Basic Functionality Tests

- Module instantiation with minimal config
- Module instantiation with full config
- Output validation
- Variable validation

### 2. Safety Validation Tests

- Production environment protection
- Probability range validation
- Maximum destructions validation
- Resource targeting validation

### 3. Integration Tests

- Mock resource creation
- Chaos logic execution
- Backup functionality
- Notification webhook testing

### 4. Security Tests

- Resource exclusion validation
- Tag-based filtering
- Region exclusion
- Age-based filtering

## Expected Test Results

### Success Cases

- ✅ Module initializes successfully
- ✅ All variable validations pass
- ✅ Outputs are properly formatted
- ✅ Safety warnings are displayed when appropriate

### Failure Cases (Expected)

- ❌ Production environment with chaos enabled should fail validation
- ❌ Invalid probability values should fail validation
- ❌ Invalid maximum destructions should fail validation
- ❌ Missing required variables should fail validation

## Test Environment Setup

### AWS Configuration

For integration tests, configure AWS credentials:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Mock Resources

The tests create mock AWS resources for the chaos monkey to target:

- EC2 instances
- S3 buckets
- RDS instances
- Lambda functions

### Cleanup

Always run `terraform destroy` after testing to clean up resources:

```bash
terraform destroy -var-file="test-variables.tfvars" -auto-approve
```

## Continuous Integration

These tests should be run in CI/CD pipelines:

1. **Pre-commit**: Run `terraform validate` and `terraform fmt`
2. **Pre-merge**: Run full test suite with mock resources
3. **Post-merge**: Integration tests in isolated environment

## Troubleshooting

### Common Issues

1. **Terraform version mismatch**: Ensure you're using Terraform >= 1.0
2. **AWS credentials**: Verify AWS credentials are properly configured
3. **State file conflicts**: Use unique state file names for parallel test runs

### Debug Mode

Enable debug logging:

```bash
export TF_LOG=DEBUG
terraform plan
```

### Test Isolation

Each test should use unique resource names to avoid conflicts:

```hcl
resource "aws_s3_bucket" "test" {
  bucket = "test-bucket-${random_pet.suffix.id}"
}
```

## Security Considerations

⚠️ **Important**: These tests create and potentially destroy real cloud resources.

- Always use test accounts
- Monitor resource usage
- Set up billing alerts
- Use resource limits
- Enable backup before testing

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Add appropriate comments
3. Include both success and failure test cases
4. Update this README with new test descriptions
5. Ensure tests are idempotent

---

*Test responsibly and always clean up after testing!*
