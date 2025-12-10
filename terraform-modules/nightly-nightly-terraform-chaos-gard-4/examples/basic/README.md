# Basic Chaos Garden Example

This example demonstrates how to use the chaos garden module with minimal configuration.

## Running this example

1. Clone the repository
2. Navigate to this example directory
3. Run `terraform init`
4. Run `terraform apply`
5. Observe the chaos garden being created
6. Run `terraform destroy` when done

## What gets created

- A chaotic S3 bucket with random naming
- A Lambda function that performs random chaos actions
- CloudWatch events to schedule chaos (if enabled)
- Outputs with URLs to monitor your chaos garden
