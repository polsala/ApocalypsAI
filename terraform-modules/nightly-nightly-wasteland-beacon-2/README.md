# Nightly Wasteland Beacon

Deploys a scheduled AWS Lambda function and associated resources to act as a "Wasteland Resource Beacon", emitting periodic status signals to CloudWatch Logs. This module provides a simple, cost-effective way to establish a minimal, observable presence in your cloud environment, simulating a beacon for survivors in a post-apocalyptic world.

## Features

*   **Scheduled Heartbeat**: An AWS Lambda function triggers on a configurable schedule.
*   **CloudWatch Logging**: All beacon signals (Lambda invocations) are logged to a dedicated CloudWatch Log Group.
*   **Minimalist Design**: Focuses on core components for low cost and easy deployment.
*   **Customizable**: Easily adjust beacon name, schedule, and AWS region.

## Usage

To deploy your Wasteland Resource Beacon, include this module in your Terraform configuration:

```terraform
module "wasteland_beacon" {
  source = "./nightly-wasteland-beacon/src" # Adjust path if not local

  beacon_name         = "my-resource-cache-beacon"
  schedule_expression = "rate(6 hours)" # e.g., "cron(0 0 * * ? *)" for daily at midnight UTC
  aws_region          = "us-east-1"
}

output "beacon_lambda_name" {
  description = "The name of the deployed Lambda function."
  value       = module.wasteland_beacon.beacon_lambda_name
}

output "beacon_log_group_name" {
  description = "The name of the CloudWatch Log Group for beacon signals."
  value       = module.wasteland_beacon.beacon_log_group_name
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to deploy the beacon.

## Module Inputs

| Name                | Description                                                               | Type     | Default | Required |
| :------------------ | :------------------------------------------------------------------------ | :------- | :------ | :------- |
| `beacon_name`       | A unique name for the beacon resources.                                   | `string` | n/a     | yes      |
| `schedule_expression` | The schedule expression for the beacon (e.g., `rate(1 hour)` or `cron(0 0 * * ? *)`). | `string` | n/a     | yes      |
| `aws_region`        | The AWS region to deploy the beacon in.                                   | `string` | n/a     | yes      |

## Module Outputs

| Name                  | Description                                            |
| :-------------------- | :----------------------------------------------------- |
| `beacon_lambda_name`  | The name of the deployed AWS Lambda function.          |
| `beacon_log_group_name` | The name of the CloudWatch Log Group for beacon signals. |

## Development & Testing

The module includes a simple test script that validates the Terraform configuration and generates a plan without deploying resources.

To run tests:

```bash
cd tests
./test.sh
```

This will perform `terraform init` and `terraform validate` and `terraform plan` to ensure the module's syntax and configuration are correct.
