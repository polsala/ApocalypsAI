# Test Suite for Nightly Terraform Void Shield

This directory contains a comprehensive test suite for the Terraform module.

## Running Tests

1. Initialize the test environment:
   ```bash
   terraform init
   ```

2. Plan the test configuration:
   ```bash
   terraform plan
   ```

3. Apply the test configuration:
   ```bash
   terraform apply -auto-approve
   ```

4. View the outputs:
   ```bash
   terraform output
   ```

5. Clean up:
   ```bash
   terraform destroy -auto-approve
   ```

## Test Coverage

The test suite validates:
- Security group name generation
- Port assignments (SSH, HTTP, HTTPS)
- Priority generation
- CIDR block handling
- Output values
- Module metadata
