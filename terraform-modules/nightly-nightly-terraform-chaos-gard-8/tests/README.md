# Testing the Chaos Garden Module

This directory contains tests for the Terraform Chaos Garden Orchestrator module.

## Test Structure

- `test_chaos_garden.tf` - Main test configuration
- `README.md` - This documentation file

## Running Tests

### Prerequisites

1. Install Terraform (version 1.0 or higher)
2. Configure AWS credentials
3. Have appropriate AWS permissions for creating resources

### Test Execution

1. **Initialize the test configuration:**
   ```bash
   cd tests
   terraform init
   ```

2. **Plan the test resources:**
   ```bash
   terraform plan
   ```

3. **Apply the test configuration:**
   ```bash
   terraform apply
   ```

4. **Verify the outputs:**
   Check that all outputs are generated correctly:
   - `test_chaos_garden_url` - Should show the API Gateway URL
   - `test_experiment_bucket` - Should show the S3 bucket name
   - `test_sns_topic` - Should show the SNS topic ARN
   - `test_lambda_arn` - Should show the Lambda function ARN

5. **Test the API endpoint:**
   ```bash
   curl https://<test_chaos_garden_url>
   ```

6. **Clean up test resources:**
   ```bash
   terraform destroy
   ```

## Test Scenarios

### Scenario 1: Basic Module Deployment
- **Purpose**: Verify that all resources are created correctly
- **Expected Results**: All resources should be created without errors
- **Mock rationale**: Uses mock AWS credentials and region for testing

### Scenario 2: API Gateway Functionality
- **Purpose**: Test the API endpoint for retrieving chaos garden status
- **Expected Results**: API should return JSON with chaos garden information
- **Mock rationale**: Uses mock Lambda function responses for testing

### Scenario 3: SNS Topic Creation
- **Purpose**: Verify that the SNS topic is created for alerts
- **Expected Results**: SNS topic should be created with correct configuration
- **Mock rationale**: Uses mock SNS service for testing

### Scenario 4: Lambda Function Deployment
- **Purpose**: Test that the Lambda function is deployed correctly
- **Expected Results**: Lambda function should be created with proper permissions
- **Mock rationale**: Uses mock Lambda service for testing

### Scenario 5: CloudWatch Integration
- **Purpose**: Verify CloudWatch metrics and alarms are configured
- **Expected Results**: CloudWatch resources should be created
- **Mock rationale**: Uses mock CloudWatch service for testing

## Test Data

The tests use the following configuration:
- **Environment**: test
- **Region**: us-west-2
- **Chaos Scenarios**: network_latency, resource_deletion, service_disruption
- **Max Concurrent Experiments**: 2
- **Experiment Duration**: 10m
- **Rollback Enabled**: true
- **Alert Email**: test@example.com

## Safety Considerations

⚠️ **Warning**: These tests create real AWS resources. Ensure you:

1. Run tests in a dedicated test account
2. Clean up resources after testing
3. Monitor AWS costs during testing
4. Never run tests against production environments

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure your AWS credentials have the necessary permissions
2. **Resource Limits**: Check AWS service limits if resources fail to create
3. **Name Conflicts**: Module names might conflict if tests were run previously

### Debug Steps

1. Check Terraform plan output for any warnings or errors
2. Verify AWS credentials are configured correctly
3. Review AWS CloudTrail logs for any API errors
4. Check AWS service quotas for the region

## Test Validation

After running the tests, validate the following:

1. ✅ All resources are created successfully
2. ✅ API Gateway endpoint is accessible
3. ✅ S3 bucket is created for experiment logs
4. ✅ SNS topic is created for alerts
5. ✅ Lambda function is deployed with correct permissions
6. ✅ CloudWatch metrics and alarms are configured
7. ✅ All outputs are generated correctly
8. ✅ Resources can be destroyed cleanly

## Continuous Integration

This module can be integrated into CI/CD pipelines by:

1. Running `terraform init` and `terraform plan` in the tests directory
2. Using the plan output to verify changes before applying
3. Running `terraform apply` in a controlled test environment
4. Cleaning up with `terraform destroy` after validation

---

*Remember: Always test in a safe environment before deploying to production!*
