# Nightly Cloud Hibernation Pod

## Overview

The `nightly-cloud-hibernation-pod` is a whimsical-yet-useful Terraform module designed to help the community conserve precious cloud resources (and credits!) in the post-apocalyptic digital wasteland. It provisions a scheduled mechanism to automatically stop and start non-critical AWS EC2 instances based on specified tags and cron schedules.

Think of it as a cozy, energy-saving pod for your digital infrastructure, ensuring your development, staging, or less-frequently-used instances take a nap when not needed and wake up refreshed.

## Features

- **Automated Scheduling**: Define cron expressions for stopping and starting EC2 instances.
- **Tag-Based Selection**: Target specific EC2 instances using AWS tags.
- **Cost & Energy Savings**: Reduce operational costs by powering down idle resources.
- **Self-Contained**: Deploys all necessary AWS resources (Lambda, IAM, CloudWatch Events).

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "hibernation_scheduler" {
  source = "./path/to/nightly-cloud-hibernation-pod/src"

  name_prefix       = "my-dev-hibernation" # Unique prefix for AWS resources
  region            = "us-east-1"          # AWS region where instances and scheduler reside
  resource_tags     = {
    "Environment" = "dev",
    "Hibernatable" = "true"
  }                                        # Instances with these tags will be managed
  stop_cron_schedule  = "cron(0 22 * * ? *)" # Stop instances daily at 10 PM UTC
  start_cron_schedule = "cron(0 8 * * ? *)"  # Start instances daily at 8 AM UTC
}

output "lambda_function_name" {
  value = module.hibernation_scheduler.lambda_function_name
}
```

## Module Inputs

| Name              | Description                                                                    | Type        | Default     | Required |
|-------------------|--------------------------------------------------------------------------------|-------------|-------------|----------|
| `name_prefix`     | A unique prefix for all created AWS resources (e.g., Lambda, IAM roles, rules). | `string`    | `hibernation-pod` | no       |
| `region`          | The AWS region where resources are located and the scheduler will operate.     | `string`    | n/a         | yes      |
| `resource_tags`   | A map of tags to identify EC2 instances to be hibernated (e.g., `{ 'Environment' = 'dev' }`). | `map(string)` | `{}`        | no       |
| `stop_cron_schedule` | The cron expression for when to stop resources (e.g., `'cron(0 22 * * ? *)'` for 10 PM UTC daily). | `string`    | n/a         | yes      |
| `start_cron_schedule`| The cron expression for when to start resources (e.g., `'cron(0 8 * * ? *)'` for 8 AM UTC daily). | `string`    | n/a         | yes      |

## Module Outputs

| Name                 | Description                                    |
|----------------------|------------------------------------------------|
| `lambda_function_name` | The name of the created AWS Lambda function.   |
| `stop_event_rule_name` | The name of the CloudWatch Event Rule for stopping instances. |
| `start_event_rule_name`| The name of the CloudWatch Event Rule for starting instances. |

## Requirements

- AWS Provider configured with appropriate credentials.
- Terraform `v1.0.0` or higher.

## Testing

To test this module, navigate to the `tests/` directory and run the `test.sh` script. This script performs `terraform init`, `validate`, and `plan` operations against a mock configuration to ensure the module is syntactically correct and generates an expected plan without deploying actual resources.

```bash
cd nightly-cloud-hibernation-pod/tests
./test.sh
```
