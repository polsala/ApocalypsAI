# Testing the Terraform Chaos Monkey Module

This directory contains comprehensive tests for the Terraform Chaos Monkey module to ensure reliability and correctness.

## Test Structure

### Python Tests (`test_chaos_monkey.py`)

Unit tests for the Lambda function logic:

- **ChaosMonkey Class Tests**: Test instance selection, chaos triggering, and execution
- **Lambda Handler Tests**: Test the main Lambda handler function
- **Mock Integration**: Use mocks to simulate AWS services without actual calls

#### Running Python Tests

```bash
# Install test dependencies
pip install -r lambda/requirements.txt

# Run tests
python -m pytest tests/test_chaos_monkey.py -v
```

### Terraform Tests (`test_terraform.py`)

Integration tests using Terratest to validate Terraform module behavior:

- **Basic Usage Test**: Test basic module configuration
- **Advanced Usage Test**: Test complex configurations with multiple options
- **Disabled Mode Test**: Test module behavior when chaos is disabled
- **Dry Run Test**: Test dry run functionality
- **Tag Filtering Test**: Test instance selection based on tags

#### Running Terraform Tests

```bash
# Install Go and Terratest dependencies
# Run tests
go test -v ./tests/
```

## Test Coverage

### Unit Tests
- ✅ Instance selection logic
- ✅ Chaos probability calculation
- ✅ Tag filtering (included/excluded)
- ✅ Dry run mode
- ✅ Error handling
- ✅ Lambda handler logic

### Integration Tests
- ✅ Terraform module deployment
- ✅ AWS resource creation (Lambda, CloudWatch, EventBridge)
- ✅ Configuration validation
- ✅ Output verification
- ✅ Environment variable setup

### Manual Testing

#### Local Development

1. **Set up AWS credentials**
   ```bash
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_DEFAULT_REGION=us-east-1
   ```

2. **Deploy test configuration**
   ```bash
   cd examples/basic-usage
   terraform init
   terraform apply
   ```

3. **Test Lambda function**
   ```bash
   # Invoke the Lambda function manually
   aws lambda invoke --function-name chaos-monkey-logger --payload '{"test": true}' response.json
   cat response.json
   ```

4. **Clean up**
   ```bash
   terraform destroy
   ```

#### CI/CD Testing

The module includes GitHub Actions workflows for automated testing:

- **Unit Tests**: Run on every pull request
- **Integration Tests**: Run on merge to main
- **Terraform Validation**: Check syntax and configuration

## Test Best Practices

### Mock Usage

- **AWS Services**: Mock EC2, SSM, CloudWatch, and Lambda calls
- **Environment Variables**: Set test-specific values
- **Random Behavior**: Mock random number generation for predictable tests

### Test Data

- **Realistic Instances**: Use realistic instance IDs and configurations
- **Edge Cases**: Test with empty lists, invalid configurations
- **Error Conditions**: Test failure scenarios and error handling

### Test Organization

- **Separate Concerns**: Unit tests vs integration tests
- **Clear Naming**: Descriptive test function names
- **Setup/Teardown**: Proper test isolation

## Troubleshooting

### Common Issues

1. **AWS Permissions**: Ensure test credentials have necessary permissions
2. **Resource Limits**: Check AWS service limits for test resources
3. **Network Connectivity**: Verify internet access for AWS API calls

### Debug Tips

1. **Enable Verbose Logging**: Set `verbose_logging = true` in test configs
2. **Check CloudWatch Logs**: Monitor Lambda execution logs
3. **Use Dry Run Mode**: Test without actual resource changes

## Contributing Tests

When adding new features:

1. **Write Tests First**: Follow TDD practices
2. **Cover Edge Cases**: Test boundary conditions
3. **Update Documentation**: Keep test docs current
4. **Run All Tests**: Ensure no regressions

## Performance Testing

### Load Testing

- **Multiple Instances**: Test with large numbers of target instances
- **High Frequency**: Test with frequent chaos triggering
- **Resource Limits**: Monitor AWS service limits

### Cost Testing

- **Lambda Invocations**: Monitor Lambda execution costs
- **CloudWatch Logs**: Monitor log storage costs
- **EventBridge Events**: Monitor event processing costs

---

*For more information, see the main [README](../README.md) and [examples](../examples/).*
