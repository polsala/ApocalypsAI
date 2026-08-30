# Nightly Cloud Compost Heap Terraform Module

## Overview

The `nightly-cloud-compost-heap` module helps you identify and manage stale, unused, or forgotten resources in your AWS environment. Think of it as a digital compost heap for your cloud infrastructure: resources that are no longer actively serving a purpose can be flagged, monitored, and eventually 'composted' (cleaned up) to reduce costs, improve security posture, and maintain a tidy cloud garden.

This module provisions AWS Config rules and an S3 bucket to facilitate the detection and logging of such resources. It focuses on common culprits like unattached EBS volumes and long-stopped EC2 instances.

## Features

*   **Stale EBS Volume Detection**: AWS Config rule to identify EBS volumes that are not attached to any EC2 instance.
*   **Stale EC2 Instance Detection**: AWS Config rule to identify EC2 instances that have been stopped for a configurable duration.
*   **Compost Bucket**: An S3 bucket to store reports, logs, or even 'quarantined' data from identified stale resources.
*   **Notification**: An SNS topic to send alerts when compostable resources are detected.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary inputs. The `source` path below assumes the module is located at `terraform-modules/nightly-cloud-compost-heap/src` relative to your root Terraform configuration.

```terraform
module "cloud_compost_heap" {
  source  = "../../terraform-modules/nightly-cloud-compost-heap/src"
  # Alternatively, if published to a registry:
  # source = "polsala/cloud-compost-heap/aws"
  # version = "1.0.0"

  project_name                      = "ApocalypsAI-Compost"
  region                            = "us-east-1"
  enable_s3_compost_bucket          = true
  enable_ebs_stale_volume_detector  = true
  enable_ec2_stale_instance_detector = true
  stale_instance_age_days           = 45 # Flag instances stopped for more than 45 days

  tags = {
    Environment = "Dev"
    ManagedBy   = "ApocalypsAI"
  }
}

output "compost_bucket_name" {
  value       = module.cloud_compost_heap.compost_bucket_id
  description = "The name of the S3 bucket for composted items."
}

output "stale_ebs_config_rule_id" {
  value       = module.cloud_compost_heap.stale_ebs_config_rule_id
  description = "The ID of the AWS Config rule for stale EBS volumes."
}

output "notification_topic_arn" {
  value       = module.cloud_compost_heap.notification_topic_arn
  description = "The ARN of the SNS topic for notifications."
}
```

## Inputs

| Name                               | Description                                                                 | Type     | Default   | Required |
| :--------------------------------- | :-------------------------------------------------------------------------- | :------- | :-------- | :------- |
| `project_name`                     | A unique name for the project, used for resource naming and tagging.        | `string` | `""`      | yes      |
| `region`                           | The AWS region where resources will be deployed.                            | `string` | `""`      | yes      |
| `enable_s3_compost_bucket`         | Whether to create an S3 bucket for composted items/reports.                 | `bool`   | `true`    | no       |
| `enable_ebs_stale_volume_detector` | Whether to create an AWS Config rule for unattached EBS volumes.            | `bool`   | `true`    | no       |
| `enable_ec2_stale_instance_detector` | Whether to create an AWS Config rule for long-stopped EC2 instances.        | `bool`   | `true`    | no       |
| `stale_instance_age_days`          | Number of days an EC2 instance must be stopped to be considered stale.      | `number` | `30`      | no       |
| `tags`                             | A map of tags to apply to all created resources.                            | `map`    | `{}`      | no       |

## Outputs

| Name                               | Description                                            |
| :--------------------------------- | :----------------------------------------------------- |
| `compost_bucket_id`                | The ID of the S3 bucket for composted items.           |
| `compost_bucket_arn`               | The ARN of the S3 bucket for composted items.          |
| `stale_ebs_config_rule_id`         | The ID of the AWS Config rule for stale EBS volumes.   |
| `stale_ebs_config_rule_arn`        | The ARN of the AWS Config rule for stale EBS volumes.  |
| `stale_ec2_config_rule_id`         | The ID of the AWS Config rule for stale EC2 instances. |
| `stale_ec2_config_rule_arn`        | The ARN of the AWS Config rule for stale EC2 instances.|
| `notification_topic_arn`           | The ARN of the SNS topic for notifications.            |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
