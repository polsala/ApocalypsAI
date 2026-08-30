# Nightly Temporal Beacon

This Terraform module deploys a serverless 'Temporal Beacon' in AWS. The beacon consists of an AWS Lambda function triggered by a CloudWatch Event Rule (cron schedule) that emits a configurable timestamped message to a CloudWatch Log Group.

It's designed to provide a simple, reliable heartbeat or a way to mark the passage of time in an otherwise chaotic environment, ensuring that 'time continues' even when other systems might falter.

## Features

*   **Scheduled Emissions**: Configurable cron-like schedule for beacon messages.
*   **Customizable Message**: Define the message the beacon emits.
*   **Serverless**: No servers to manage, scales automatically, cost-effective.
*   **Log Stream**: All beacon emissions are logged to a dedicated CloudWatch Log Group.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "temporal_beacon" {
  source = "./terraform-modules/nightly-temporal-beacon/src"

  beacon_name         = "my-apocalypsai-beacon"
  schedule_expression = "rate(1 hour)" # e.g., "cron(0 12 * * ? *)" for daily at noon UTC
  beacon_message      = "ApocalypsAI Temporal Beacon: All systems are go. The future is now."
  aws_region          = "us-east-1"
}

output "beacon_lambda_name" {
  value       = module.temporal_beacon.lambda_function_name
  description = "The name of the deployed Lambda function."
}

output "beacon_log_group" {
  value       = module.temporal_beacon.cloudwatch_log_group_name
  description = "The name of the CloudWatch Log Group where beacon messages are sent."
}
```

## Requirements

*   Terraform CLI (v1.0+)
*   AWS Account and configured AWS CLI credentials with permissions to create Lambda functions, IAM roles, and CloudWatch resources.

## Inputs

| Name                | Description                                       | Type     | Default                                                              | Required |
| :------------------ | :------------------------------------------------ | :------- | :------------------------------------------------------------------- | :------- |
| `beacon_name`       | A unique name for the temporal beacon resources.  | `string` | `"temporal-beacon"`                                                | no       |
| `schedule_expression` | The CloudWatch Event Rule schedule expression.    | `string` | `"rate(1 hour)"`                                                   | no       |
| `beacon_message`    | The message the beacon will emit.                 | `string` | `"Temporal Beacon: All systems nominal. Time continues."`            | no       |
| `aws_region`        | The AWS region to deploy the beacon resources in. | `string` | `"us-east-1"`                                                      | no       |

## Outputs

| Name                        | Description                                     |
| :-------------------------- | :---------------------------------------------- |
| `lambda_function_name`      | The name of the deployed AWS Lambda function.   |
| `cloudwatch_log_group_name` | The name of the CloudWatch Log Group for logs.  |

## Development

The Lambda function code is located in `src/lambda/beacon.py`. The Terraform configuration is in `src/main.tf`, `src/variables.tf`, and `src/outputs.tf`.

To run tests, execute `tests/test_module.sh`.
