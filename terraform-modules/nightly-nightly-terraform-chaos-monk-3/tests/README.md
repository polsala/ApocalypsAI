# Tests for Nightly Terraform Chaos Monkey

This directory contains unit tests for the chaos monkey lambda function.

## Test Structure

- `test_chaos_monkey.py` - Main test suite for the lambda function

## Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.test_chaos_monkey.TestChaosMonkey.test_handler_success

# Run with coverage
coverage run -m unittest discover tests/
coverage report
```

## Test Coverage

The tests cover:

- **Handler Function**: Main execution flow and error handling
- **EC2 Chaos**: Instance termination in dry run and protected modes
- **RDS Chaos**: Database deletion in dry run and protected modes
- **Lambda Chaos**: Function deletion in dry run and protected modes
- **Error Handling**: Exception scenarios and edge cases
- **Environment Variables**: Parsing and configuration

## Mock Rationale

- **AWS Clients**: Mocked to avoid actual cloud resource manipulation during testing
- **Environment Variables**: Set to known values for consistent test behavior
- **Random Selection**: Controlled through deterministic test data

## Test Data

Test data includes:
- Mock AWS resource responses
- Protected resource lists
- Dry run configurations
- Error scenarios

## Best Practices

- Tests are isolated and don't depend on external resources
- All AWS API calls are mocked
- Tests verify both success and failure scenarios
- Dry run mode is extensively tested to ensure safety
- Protected resources are never targeted in tests
