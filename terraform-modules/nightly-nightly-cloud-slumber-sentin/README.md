# Nightly Cloud Slumber Sentinel

A whimsical-yet-useful Terraform module designed to gently guide your AWS EC2 instances into a cost-saving slumber during off-peak hours and awaken them refreshed for the new day. This utility helps optimize your cloud spend by automatically stopping non-critical instances when they're not needed and restarting them on schedule.

## Features

*   **Scheduled Hibernation**: Define specific cron schedules for stopping and starting EC2 instances.
*   **Tag-Based Selection**: Target instances using AWS tags, allowing flexible management of your fleet.
*   **Cost Optimization**: Reduce your AWS bill by only running instances when necessary.
*   **Whimsical Naming**: Embrace the "slumber" theme for your infrastructure automation.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "slumber_sentinel" {
  source = "./path/to/nightly-cloud-slumber-sentinel/src" # Or a Git/registry source

  # Required
  aws_region          = "us-east-1"
  instance_tags       = {
    "Environment" = "dev",
    "Slumber"     = "true"
  }
  stop_cron_schedule  = "cron(0 22 * * ? *)" # Every day at 10 PM UTC
  start_cron_schedule = "cron(0 7 * * ? *)"  # Every day at 7 AM UTC

  # Optional
  lambda_memory_size  = 128 # Default is 128
  lambda_timeout      = 60  # Default is 60
}
```

### Inputs

| Name                | Description                                                                                             | Type     | Default | Required |
| :------------------ | :------------------------------------------------------------------------------------------------------ | :------- | :------ | :------- |
| `aws_region`        | The AWS region where the resources will be deployed.                                                    | `string` | n/a     | yes      |
| `instance_tags`     | A map of tags to identify the EC2 instances that should be managed by the sentinel.                     | `map(string)` | n/a     | yes      |
| `stop_cron_schedule`| The cron expression for when instances should enter their slumber (stop). Example: `cron(0 22 * * ? *)` | `string` | n/a     | yes      |
| `start_cron_schedule`| The cron expression for when instances should awaken (start). Example: `cron(0 7 * * ? *)`             | `string` | n/a     | yes      |
| `lambda_memory_size`| The memory size for the AWS Lambda function in MB.                                                      | `number` | `128`   | no       |
| `lambda_timeout`    | The timeout for the AWS Lambda function in seconds.                                                     | `number` | `60`    | no       |

### Outputs

| Name                      | Description                                     |
| :------------------------ | :---------------------------------------------- |
| `slumber_lambda_arn`      | The ARN of the EC2 Slumber Manager Lambda function. |
| `stop_event_rule_arn`     | The ARN of the CloudWatch Event Rule for stopping instances. |
| `start_event_rule_arn`    | The ARN of the CloudWatch Event Rule for starting instances. |

## How it Works

1.  **Lambda Function**: A Python-based AWS Lambda function is deployed. This function takes `instance_tags` and an `action` (`stop` or `start`) as input. It then uses the AWS SDK (boto3) to find EC2 instances matching the provided tags and performs the specified action.
2.  **CloudWatch Event Rules**: Two CloudWatch Event Rules are created.
    *   One rule is configured with `stop_cron_schedule` and targets the Lambda function with a payload instructing it to `stop` instances.
    *   The second rule is configured with `start_cron_schedule` and targets the Lambda function with a payload instructing it to `start` instances.
3.  **IAM Role**: An IAM role with necessary permissions (e.g., `ec2:DescribeInstances`, `ec2:StopInstances`, `ec2:StartInstances`, `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`) is created for the Lambda function.

## Development & Testing

This module includes a basic test setup to validate its syntax and ensure a valid Terraform plan can be generated.

To run tests:

1.  Navigate to the `tests/` directory.
2.  Run `./test_plan.sh`.

This script will initialize Terraform, validate the module's configuration, and attempt to generate a plan without applying any changes to your AWS account.

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.
