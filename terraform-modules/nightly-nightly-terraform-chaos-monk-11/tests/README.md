# Tests for Nightly Terraform Chaos Monkey

This directory contains tests for the chaos monkey module.

## Test Structure

```
tests/
├── terraform/
│   └── test_basic.tf          # Terraform configuration tests
├── lambda/
│   ├── test_chaos_monkey.py   # Lambda function unit tests
│   └── requirements.txt       # Test dependencies
└── README.md                # This file
```

## Running Tests

### Terraform Tests

```bash
# Initialize and plan the test configuration
cd tests/terraform
terraform init
terraform plan
```

### Lambda Tests

```bash
# Install test dependencies
pip install -r tests/lambda/requirements.txt

# Run unit tests
cd tests/lambda
python -m unittest test_chaos_monkey.py -v
```

## Test Coverage

The tests cover:

- **Resource Discovery**: EC2, RDS, and ElastiCache instance discovery
- **Tag Filtering**: Exclusion logic based on resource tags
- **Target Selection**: Random selection of chaos targets
- **Resource Termination**: Mocked termination of different resource types
- **Error Handling**: Graceful handling of API errors
- **Dry Run Mode**: Verification that dry run mode doesn't actually terminate resources
- **Lambda Handler**: End-to-end testing of the main Lambda function

## Mock Strategy

# Mock rationale: All AWS SDK calls are mocked to avoid actual resource manipulation during testing
# Mock rationale: Environment variables are mocked to control test scenarios
# Mock rationale: SNS notifications are mocked to prevent actual email sending

## Safety in Testing

- All tests use mocked AWS services
- No actual resources are created or terminated during testing
- Dry run mode is extensively tested to ensure safety
- Error conditions are simulated to test error handling

## Adding New Tests

When adding new functionality:

1. Add unit tests for new functions
2. Mock any external dependencies
3. Test both success and failure scenarios
4. Ensure dry run mode works correctly for new features
5. Update this README if new test types are added
