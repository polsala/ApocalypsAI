# Chaos Garden Test Suite

This directory contains tests for the Terraform Chaos Garden module.

## Test Structure

- `test_basic_garden.sh` - Integration test that deploys and validates the basic garden example
- `README.md` - This documentation file

## Running Tests

### Prerequisites

- Terraform >= 1.0
- AWS CLI configured with appropriate permissions
- jq (JSON processor)
- Python 3.9+ (for Lambda function packaging)

### Execute Integration Test

```bash
cd tests/
chmod +x test_basic_garden.sh
./test_basic_garden.sh
```

## Test Coverage

The integration test verifies:

1. **Terraform Operations**
   - `terraform init` succeeds
   - `terraform plan` succeeds
   - `terraform apply` succeeds
   - `terraform destroy` succeeds

2. **Resource Creation**
   - Correct number of EC2 instances
   - Correct number of Lambda functions
   - Correct number of S3 buckets
   - Correct number of RDS instances (0 in basic example)

3. **Configuration Validation**
   - Garden name generation
   - Chaos schedule configuration
   - Cleanup schedule configuration
   - Output values correctness

4. **Safety Checks**
   - No unexpected resource creation
   - Proper cleanup after test
   - Resource count matches expectations

## Test Environment

**IMPORTANT**: Always run tests in a dedicated AWS account or sandbox environment.

### Recommended Test Account Setup

- Use AWS Organizations SCPs to limit spending
- Enable billing alerts
- Use IAM roles with minimal required permissions
- Test in us-east-1 region (default)

## Lambda Function Testing

To test Lambda functions locally:

```bash
# Package Lambda functions
zip -r lambda/chaos_pollinator.zip lambda/chaos_pollinator.py
zip -r lambda/cleanup_garden.zip lambda/cleanup_garden.py

# Test with AWS SAM (optional)
aws lambda invoke --function-name test-function --payload '{}' response.json
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure AWS CLI is configured with appropriate permissions
   - Check IAM policies for EC2, Lambda, S3, RDS, CloudWatch access

2. **Resource Limits**
   - Check AWS service limits for EC2 instances, RDS instances, etc.
   - Request limit increases if needed

3. **Terraform Errors**
   - Ensure Terraform version >= 1.0
   - Check for provider version conflicts
   - Verify AWS region is correct

### Debug Mode

Run tests with debug output:

```bash
set -x
./test_basic_garden.sh
```

### Cleanup After Failed Tests

If tests fail and leave resources:

```bash
# Manual cleanup script (use with caution)
aws ec2 describe-instances --filters "Name=tag:Garden,Values=apocalypsi-chaos-garden" --query 'Reservations[].Instances[].InstanceId' --output text | xargs -I {} aws ec2 terminate-instances --instance-ids {}

aws s3api list-buckets --query 'Buckets[?contains(Name, `apocalypsi-chaos-garden`)].Name' --output text | xargs -I {} aws s3 rb s3://{} --force

aws rds describe-db-instances --query 'DBInstances[?contains(DBInstanceIdentifier, `apocalypsi-chaos-garden`)].DBInstanceIdentifier' --output text | xargs -I {} aws rds delete-db-instance --db-instance-identifier {} --skip-final-snapshot --delete-automated-backups
```

## Contributing

When adding new tests:

1. Follow the existing naming convention
2. Add appropriate documentation
3. Ensure tests are idempotent
4. Include cleanup procedures
5. Test in isolated environment first

## Test Data

Test data is mocked using:
- Terraform's built-in random providers
- AWS provider data sources for AMIs
- Local execution without external dependencies

**Mock rationale**: Using real AWS resources for testing would incur costs and create dependencies on external services. The current approach allows for cost-effective, reliable testing while maintaining functionality validation.
