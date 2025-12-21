# Nightly Cloud Resource Guardian

## Overview

The `nightly-cloud-resource-guardian` Terraform module provisions a set of essential, low-cost AWS cloud resources designed to establish a baseline of "post-apocalyptic cloud hygiene." In an unpredictable world, ensuring your foundational cloud infrastructure is secure, monitored, and properly tagged is paramount. This module helps you set up a secure S3 bucket for vital data, an SNS topic for critical alerts, and a CloudWatch alarm to monitor your AWS budget.

## Features

*   **Secure S3 Bucket**: A private S3 bucket with server-side encryption (AES256), versioning, and public access blocking enabled by default, ideal for storing critical logs, backups, or survival manifests.
*   **SNS Alerting Topic**: A dedicated Amazon SNS topic for receiving notifications from monitoring systems, such as the budget alarm.
*   **CloudWatch Budget Alarm**: An AWS CloudWatch alarm that triggers if your estimated AWS charges exceed a specified threshold, helping you keep an eye on resource consumption even when other systems might fail.
*   **Standardized Tagging**: All resources are tagged with `Project`, `Environment`, `ManagedBy`, and `Purpose` for easy identification, cost allocation, and management.

## Why is this useful?

Even in the most chaotic scenarios, maintaining a minimal, secure, and observable cloud footprint is crucial. This module provides a quick, repeatable way to deploy these foundational elements, ensuring you have a place to store critical information, receive alerts about unexpected costs, and maintain basic control over your cloud resources.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

### Prerequisites

*   Terraform CLI installed (v1.0+)
*   AWS CLI configured with appropriate credentials and permissions to create S3 buckets, SNS topics, and CloudWatch alarms.

### Example Configuration

Create a `main.tf` file in your root module:

```terraform
provider "aws" {
  region = "us-east-1"
}

module "survival_guardian" {
  source  = "./modules/nightly-cloud-resource-guardian" # Adjust path if not using local module
  project_name     = "ApocalypsAI"
  environment      = "production"
  budget_threshold = 50 # USD
}

output "survival_bucket_arn" {
  value       = module.survival_guardian.s3_bucket_arn
  description = "The ARN of the secure S3 survival cache bucket."
}

output "alert_sns_topic_arn" {
  value       = module.survival_guardian.sns_topic_arn
  description = "The ARN of the SNS topic for alerts."
}

output "budget_alarm_arn" {
  value       = module.survival_guardian.cloudwatch_alarm_arn
  description = "The ARN of the CloudWatch budget alarm."
}
```

### Running Terraform

1.  Initialize Terraform:
    ```bash
    terraform init
    ```
2.  Review the plan:
    ```bash
    terraform plan
    ```
3.  Apply the changes:
    ```bash
    terraform apply
    ```

## Inputs

| Name               | Description                                                               | Type     | Default       | Required |
| :----------------- | :------------------------------------------------------------------------ | :------- | :------------ | :------- |
| `project_name`     | The name of the project to associate with these resources.                | `string` | `"apocalypsai"` | no       |
| `environment`      | The deployment environment (e.g., `dev`, `staging`, `production`).      | `string` | `"production"` | no       |
| `budget_threshold` | The maximum estimated monthly AWS charges (in USD) before the alarm triggers. | `number` | `100`         | no       |

## Outputs

| Name                    | Description                                       |
| :---------------------- | :------------------------------------------------ |
| `s3_bucket_arn`         | The ARN of the secure S3 survival cache bucket.   |
| `sns_topic_arn`         | The ARN of the SNS topic for alerts.              |
| `cloudwatch_alarm_arn`  | The ARN of the CloudWatch budget alarm.           |

## Development & Testing

This module includes automated tests that verify the planned infrastructure without deploying actual resources. See `tests/test_plan_output.sh` for details.
