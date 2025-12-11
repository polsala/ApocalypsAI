# Basic Chaos Garden Example

This example demonstrates a basic chaos garden with minimal resources for testing and learning.

## Resources Created

- 2 EC2 instances (t3.micro)
- 1 Lambda function for chaos experiments
- 1 S3 bucket
- CloudWatch events for chaos scheduling and cleanup
- CloudWatch dashboard and alarms

## Usage

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply

# Destroy when done
terraform destroy
```

## Safety Notes

- This example disables RDS to reduce costs
- Cleanup runs daily at 2 AM to prevent resource accumulation
- Chaos experiments run every 2 hours
- Always use in a dedicated AWS account or sandbox environment
