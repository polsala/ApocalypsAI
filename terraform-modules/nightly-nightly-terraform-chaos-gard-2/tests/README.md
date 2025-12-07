# Testing the Chaos Garden Module

This directory contains tests for the Terraform Chaos Garden module.

## Test Structure

- `test_main.tf`: Basic test configuration that verifies the module can be planned and applied
- `README.md`: This documentation file

## Running Tests

1. **Prerequisites**:
   - Terraform 1.0+
   - AWS CLI configured with appropriate permissions
   - Access to AWS services (EC2, S3, VPC, etc.)

2. **Basic Test**:
   ```bash
   cd tests
   terraform init
   terraform plan -var-file="test.tfvars"
   terraform apply -var-file="test.tfvars" -auto-approve
   ```

3. **Cleanup**:
   ```bash
   terraform destroy -var-file="test.tfvars" -auto-approve
   ```

## Test Configuration

The test uses a `test.tfvars` file (not included in the module) with the following structure:

```hcl
region = "us-east-1"
environment = "test"
chaos_level = "low"
enable_network_chaos = true
enable_compute_chaos = true
enable_storage_chaos = true
instance_count = 1
notification_email = "test@example.com"
destroy_after_hours = 1
tags = {
  test = "true"
  purpose = "chaos-garden-testing"
}
```

## Test Scenarios

1. **Low Chaos Level**: Tests basic resource creation with minimal chaos
2. **Medium Chaos Level**: Tests moderate chaos patterns
3. **High Chaos Level**: Tests maximum chaos including RDS and Redshift

## Safety Considerations

- Tests should only be run in isolated AWS accounts
- All resources are tagged with `chaos_garden=true` for easy identification
- Auto-cleanup is enabled in tests to prevent resource accumulation
- Tests use minimal resource counts to reduce cost

## Expected Test Results

- All resources should be created successfully
- All outputs should be generated correctly
- All resources should be properly tagged
- Cleanup should remove all resources

## Mock Rationale

For automated testing without actual AWS resources, you could mock:
- AWS API responses for resource creation
- Terraform plan/apply operations
- Cost estimation calculations
- Resource dependency resolution

This would allow testing the module logic without incurring AWS charges.
