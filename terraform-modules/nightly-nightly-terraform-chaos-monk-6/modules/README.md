# Chaos Monkey Modules

This directory contains reusable Terraform modules for the Chaos Monkey system.

## Modules

### chaos-monkey

Main Chaos Monkey module that creates all necessary resources:

- Lambda function with chaos logic
- IAM roles and policies
- CloudWatch Event scheduling
- SNS notifications
- CloudWatch metrics and dashboards
- Logging and monitoring

### chaos-monkey-aws

AWS-specific implementation of the Chaos Monkey module.

### chaos-monkey-azure

Azure-specific implementation (future enhancement).

### chaos-monkey-gcp

Google Cloud Platform-specific implementation (future enhancement).

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Required variables
  prefix = "my-chaos"
  enabled = true
  
  # Optional variables
  chaos_intensity = 10
  target_resources = ["aws_instance", "aws_rds_instance"]
  safe_mode = false
}
```

## Module Inputs

See the main module's `variables.tf` for all available input variables.

## Module Outputs

See the main module's `outputs.tf` for all available output values.

## Contributing

To add new modules:

1. Create a new directory under `modules/`
2. Add `main.tf`, `variables.tf`, and `outputs.tf`
3. Update this README with module documentation
4. Add tests in the module directory

## Testing

Each module should include:

- Unit tests using Terratest
- Integration tests
- Documentation tests
- Example configurations

Run tests with:

```bash
# Install Terratest
go get github.com/gruntwork-io/terratest/modules/terraform

# Run tests
cd modules/chaos-monkey
go test -v
```

## Security

All modules follow security best practices:

- Least privilege IAM policies
- Secure defaults
- Input validation
- Audit logging
- Resource tagging

## Monitoring

All modules include:

- CloudWatch metrics
- SNS notifications
- Error handling
- Health checks
- Dashboard creation

## Support

For support and questions, please open an issue in this repository.
