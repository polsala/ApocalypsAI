# Terraform Chaos Garden Tests

This directory contains tests for the Terraform Chaos Garden module.

## Test Structure

- `test_chaos_garden.tf`: Main test configuration that validates the module
- `README.md`: This file

## Running Tests

1. **Prerequisites**:
   - Terraform >= 1.0
   - AWS CLI configured (for real tests)
   - AWS credentials with appropriate permissions

2. **Run the tests**:
   ```bash
   cd tests
   terraform init
   terraform plan
   terraform apply -auto-approve
   ```

3. **Verify outputs**:
   - Check the Terraform outputs for expected values
   - Verify that resources were created successfully

4. **Clean up**:
   ```bash
   terraform destroy -auto-approve
   ```

## Test Coverage

The tests cover:

- **Resource Creation**: Validates that all resources are created correctly
- **Output Verification**: Checks that all expected outputs are present
- **Validation Tests**: Ensures input validation works properly
- **Chaos Scenarios**: Tests that chaos scenarios are configured correctly

## Mocking Strategy

For testing without actual AWS calls, the Lambda function uses mock data:

- Mock EC2 instances
- Mock RDS instances
- Mock Lambda functions

This allows for unit testing of the Lambda logic without requiring AWS resources.

## Test Scenarios

### Low Chaos Level
- Creates basic resources
- Simulates minimal chaos

### Medium Chaos Level
- Creates all resources
- Simulates moderate chaos
- Tests Lambda overload scenarios

### High Chaos Level
- Creates all resources
- Simulates maximum chaos
- Tests all chaos scenarios

## Expected Results

- **Chaos Garden ID**: A unique identifier with 3 parts
- **EC2 Instances**: 2 instances created
- **S3 Buckets**: 1 bucket created
- **RDS Instances**: 1 instance created
- **Lambda Functions**: 1 function created
- **VPC**: A new VPC created
- **Security Group**: A security group with appropriate rules
- **CloudWatch Dashboard**: A dashboard for monitoring

## Troubleshooting

If tests fail:

1. Check AWS credentials and permissions
2. Verify Terraform version compatibility
3. Review Terraform plan output for errors
4. Check AWS console for resource creation status

## Security Considerations

- The test module creates real AWS resources
- Ensure proper IAM permissions are in place
- Clean up resources after testing
- Monitor AWS billing for test resource usage
