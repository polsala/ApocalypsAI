# Nightly Temporal Rift Monitor

A whimsical-yet-useful Terraform module to deploy a serverless function that periodically "monitors" for simulated temporal rifts in the cloud, reporting its findings.

## 🌌 What is a Temporal Rift Monitor?

In the post-apocalyptic future, temporal stability is paramount. This module deploys a vigilant AWS Lambda function, scheduled to run at regular intervals, to detect deviations from a "stable" timeline. While it won't actually prevent paradoxes, it serves as a delightful demonstration of infrastructure-as-code for scheduled serverless tasks.

## ✨ Features

*   **Serverless Deployment**: Deploys an AWS Lambda function without managing servers.
*   **Scheduled Monitoring**: Uses AWS CloudWatch Event Rules to trigger the Lambda on a configurable schedule.
*   **Whimsical Rift Detection**: The Lambda function compares the current time against a user-defined "stable time" and reports if a "temporal rift" (significant time deviation) is detected.
*   **Configurable**: Easily adjust the monitoring schedule, stable time reference, and rift detection threshold.
*   **Self-contained**: All necessary AWS resources (Lambda, IAM Role, S3 for code, CloudWatch Rule) are provisioned by this module.

## 🚀 Usage

This module is designed to be used as a submodule in your Terraform configurations.

### Prerequisites

*   An AWS account configured with appropriate credentials.
*   Terraform CLI installed.
*   `jq` installed (for running tests).

### Example Configuration

```terraform
provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "temporal_rift_monitor" {
  source = "path/to/nightly-temporal-rift-monitor/src" # Adjust this path

  prefix         = "apocalypsai-prod"
  s3_bucket_name = "apocalypsai-rift-monitor-code-bucket-prod" # Must be globally unique
  schedule_expression = "rate(30 minutes)" # Check every 30 minutes
  stable_time = "2023-01-01T00:00:00Z" # Reference point for temporal stability
  rift_threshold_seconds = 7200 # Detect a rift if deviation is > 2 hours
}

output "monitor_lambda_name" {
  value = module.temporal_rift_monitor.lambda_function_name
}

output "monitor_schedule_rule" {
  value = module.temporal_rift_monitor.cloudwatch_event_rule_name
}
```

### Inputs

| Name                     | Description                                                                                             | Type   | Default                 | Required |
| :----------------------- | :------------------------------------------------------------------------------------------------------ | :----- | :---------------------- | :------- |
| `prefix`                 | A prefix for all resources created by this module to ensure uniqueness and organization.                | `string` | `"apocalypsai"`        | no       |
| `s3_bucket_name`         | The name of the S3 bucket to store the Lambda code. **Must be globally unique.**                        | `string` | n/a                     | yes      |
| `schedule_expression`    | The CloudWatch schedule expression (e.g., `"rate(5 minutes)"` or `"cron(0 0 * * ? *)"`).                | `string` | `"rate(15 minutes)"`    | no       |
| `stable_time`            | The ISO 8601 formatted string representing the 'stable' time for rift detection (e.g., `"2000-01-01T00:00:00Z"`). | `string` | `"2000-01-01T00:00:00Z"` | no       |
| `rift_threshold_seconds` | The time difference in seconds beyond which a 'temporal rift' is detected.                              | `number` | `3600` (1 hour)         | no       |

### Outputs

| Name                          | Description                                |
| :---------------------------- | :----------------------------------------- |
| `lambda_function_name`        | The name of the deployed Lambda function.  |
| `cloudwatch_event_rule_name`  | The name of the CloudWatch Event Rule.     |

## 🧪 Testing

The tests for this module are designed to be run offline using `terraform plan -json` and `jq` to verify the expected resources are part of the plan.

To run the tests:

```bash
cd nightly-temporal-rift-monitor/tests
./test_output.sh
```

This script will:
1.  Initialize Terraform in the test directory.
2.  Generate a Terraform plan in JSON format.
3.  Use `jq` to assert that `aws_lambda_function`, `aws_cloudwatch_event_rule`, `aws_s3_bucket`, and `aws_iam_role` resources are marked for creation.
4.  Verify the names of the Lambda function and CloudWatch Event Rule match the expected values based on the test configuration.

**Mock rationale**: The `test_output.sh` script leverages `terraform plan -json` to simulate a deployment without making actual API calls to AWS. This allows for deterministic and offline testing of the module's resource definitions and outputs. `jq` is used to parse the local JSON plan output, acting as a mock for inspecting the state of the infrastructure without requiring live cloud resources.
