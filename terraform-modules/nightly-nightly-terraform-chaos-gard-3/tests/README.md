# Testing the Chaos Garden

This directory contains tests for the Terraform Chaos Garden module.

## Prerequisites

- Docker and Docker Compose for running LocalStack
- Terraform 1.0+

## Running Tests

1. Start LocalStack:
   ```bash
   docker-compose up -d
   ```

2. Initialize and run tests:
   ```bash
   terraform init
   terraform apply -auto-approve
   ```

3. Clean up:
   ```bash
   terraform destroy -auto-approve
   docker-compose down
   ```

## Test Coverage

- Resource creation (S3, DynamoDB, Lambda)
- Chaos destruction mechanism
- CloudWatch dashboard creation
- Output validation
- Mock AWS resources for offline testing
