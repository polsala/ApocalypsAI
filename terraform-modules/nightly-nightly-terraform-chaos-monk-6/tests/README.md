# Chaos Monkey Tests

This directory contains comprehensive tests for the Chaos Monkey Terraform module.

## Test Structure

```
tests/
├── README.md                    # This file
├── unit/                       # Unit tests
│   ├── test_variables.py      # Variable validation tests
│   ├── test_outputs.py        # Output validation tests
│   └── test_resources.py      # Resource creation tests
├── integration/               # Integration tests
│   ├── test_chaos_execution.py # Chaos execution tests
│   ├── test_safety_features.py # Safety feature tests
│   └── test_monitoring.py     # Monitoring tests
├── examples/                  # Example configuration tests
│   ├── test_basic.py         # Basic example tests
│   ├── test_production.py    # Production example tests
│   └── test_development.py   # Development example tests
└── fixtures/                 # Test fixtures and mock data
    ├── mock_resources.json   # Mock AWS resources
    ├── test_configurations.tfvars # Test configuration files
    └── expected_outputs.json # Expected test outputs
```

## Running Tests

### Prerequisites

1. Install Python 3.11+
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Terraform
4. Configure AWS credentials

### Unit Tests

```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Run specific unit test
python -m pytest tests/unit/test_variables.py -v
```

### Integration Tests

```bash
# Run all integration tests
python -m pytest tests/integration/ -v

# Run specific integration test
python -m pytest tests/integration/test_chaos_execution.py -v
```

### Example Tests

```bash
# Run all example tests
python -m pytest tests/examples/ -v

# Run specific example test
python -m pytest tests/examples/test_basic.py -v
```

### Full Test Suite

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Categories

### Unit Tests

- **Variable Validation**: Test all input variable validations
- **Output Validation**: Test all output value correctness
- **Resource Creation**: Test that all required resources are created

### Integration Tests

- **Chaos Execution**: Test actual chaos execution logic
- **Safety Features**: Test safe mode, excluded tags, and other safety features
- **Monitoring**: Test CloudWatch metrics, alarms, and dashboards

### Example Tests

- **Basic Configuration**: Test basic example configuration
- **Production Configuration**: Test production example configuration
- **Development Configuration**: Test development example configuration

## Test Data

### Mock Resources

The `fixtures/mock_resources.json` file contains mock AWS resources for testing:

```json
{
  "ec2_instances": [
    {
      "InstanceId": "i-1234567890abcdef0",
      "State": {"Name": "running"},
      "Tags": [
        {"Key": "Name", "Value": "test-instance"},
        {"Key": "Environment", "Value": "test"}
      ]
    }
  ],
  "rds_instances": [
    {
      "DBInstanceIdentifier": "test-db",
      "DBInstanceStatus": "available",
      "TagList": [
        {"Key": "Name", "Value": "test-db"},
        {"Key": "Environment", "Value": "test"}
      ]
    }
  ]
}
```

### Test Configurations

The `fixtures/test_configurations.tfvars` file contains various test configurations:

```hcl
# Basic test configuration
basic_config = {
  prefix = "test-chaos"
  enabled = true
  chaos_intensity = 5
  safe_mode = true
  target_resources = ["aws_instance"]
}

# Production test configuration
production_config = {
  prefix = "prod-test-chaos"
  enabled = true
  chaos_intensity = 2
  safe_mode = false
  target_resources = ["aws_instance", "aws_rds_instance"]
}

# Development test configuration
development_config = {
  prefix = "dev-test-chaos"
  enabled = true
  chaos_intensity = 20
  safe_mode = true
  dry_run_only = true
  target_resources = ["aws_instance", "aws_rds_instance", "aws_ecs_service"]
}
```

## Test Coverage

### Required Coverage

- **Unit Tests**: 90%+ coverage
- **Integration Tests**: All major features tested
- **Example Tests**: All example configurations tested
- **Edge Cases**: Boundary conditions and error scenarios

### Coverage Reporting

```bash
# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html
```

## Continuous Integration

Tests are automatically run on:

- **Pull Requests**: All tests must pass
- **Push to main**: Full test suite
- **Scheduled**: Nightly test runs

## Test Best Practices

### Mocking

- Use mocks for AWS API calls
- Mock external dependencies
- Use real Terraform for infrastructure tests

### Isolation

- Each test should be independent
- Clean up resources after tests
- Use unique test identifiers

### Assertions

- Test both positive and negative cases
- Validate error conditions
- Check resource states and configurations

### Documentation

- Document test purpose and expected behavior
- Include setup and teardown instructions
- Update tests when functionality changes

## Troubleshooting

### Common Issues

1. **AWS Credentials**: Ensure AWS credentials are configured
2. **Terraform Version**: Use Terraform 1.0+
3. **Python Dependencies**: Install all required packages
4. **Resource Limits**: Check AWS service limits

### Debug Mode

```bash
# Run tests in debug mode
python -m pytest tests/ -v -s --tb=long

# Enable debug logging
export TF_LOG=DEBUG
```

### Test Cleanup

```bash
# Clean up test resources
python cleanup_test_resources.py

# Reset test state
python reset_test_state.py
```

## Contributing

When adding new tests:

1. Follow existing test patterns
2. Add appropriate test documentation
3. Ensure tests are deterministic
4. Update test coverage requirements
5. Run the full test suite before submitting

## Support

For test-related issues, please:

1. Check the troubleshooting section
2. Review test logs and outputs
3. Open an issue with detailed information
4. Include test configuration and environment details
