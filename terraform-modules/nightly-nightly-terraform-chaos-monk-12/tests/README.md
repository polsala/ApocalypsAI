# Chaos Monkey Tests

This directory contains tests for the Terraform Chaos Monkey module.

## Test Structure

- **test_basic.tf**: Basic functionality tests
- **test_integration.tf**: Integration tests with real resources
- **test_security.tf**: Security and safety tests

## Running Tests

1. **Basic tests**
   ```bash
   cd tests
   terraform init
   terraform plan
   ```

2. **Integration tests** (requires AWS credentials)
   ```bash
   cd tests
   terraform init
   terraform apply -var="test_integration=true"
   ```

3. **Security tests**
   ```bash
   cd tests
   terraform init
   terraform plan -var="test_security=true"
   ```

## Test Coverage

- Chaos enabled/disabled states
- Dry run vs actual execution
- Resource exclusions
- Multiple resource types
- Safety mechanisms
- Error handling

## Test Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `test_integration` | `bool` | `false` | Run integration tests with real resources |
| `test_security` | `bool` | `false` | Run security and safety tests |
| `test_dry_run` | `bool` | `true` | Force dry run mode for all tests |

## Test Results

All tests should pass with:
- No actual resource destruction in dry run mode
- Proper resource exclusion handling
- Correct chaos scheduling
- Appropriate error messages for invalid configurations

## Cleanup

```bash
terraform destroy
```
