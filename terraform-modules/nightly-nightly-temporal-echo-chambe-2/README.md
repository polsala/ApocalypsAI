# Nightly Temporal Echo Chamber (Terraform Module)

This Terraform module provisions a highly resilient, message echoing system designed to capture and persist critical temporal logs across localized disruptions. It leverages AWS SQS for message queuing and S3 for durable archiving, providing a robust backbone for ApocalypsAI's distributed logging needs.

## Features

*   **Primary SQS Queue**: For ingesting temporal log messages.
*   **Dead Letter Queue (DLQ)**: Automatically configured for the primary queue to capture messages that fail processing, ensuring no data is lost.
*   **S3 Archive Bucket**: A dedicated S3 bucket for long-term, durable storage of echoed messages, acting as a historical record.
*   **Regional Resilience**: While deployed in a single region, the design facilitates easy replication across multiple AWS regions to achieve true multi-region redundancy for critical data.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "temporal_echo_chamber" {
  source = "./path/to/nightly-temporal-echo-chamber-tf"

  project_name = "apocalypsai-core"
  environment  = "production"
  region       = "us-east-1" # Or your desired AWS region
}

output "echo_chamber_queue_url" {
  value = module.temporal_echo_chamber.main_queue_url
}

output "echo_chamber_archive_bucket_name" {
  value = module.temporal_echo_chamber.archive_bucket_name
}
```

## Inputs

| Name         | Description                                       | Type     | Default       | Required |
|--------------|---------------------------------------------------|----------|---------------|----------|
| `project_name` | The name of the project, used for resource naming. | `string` | `apocalypsai` | no       |
| `environment`  | The deployment environment (e.g., `dev`, `prod`). | `string` | `dev`         | no       |
| `region`       | The AWS region to deploy resources into.          | `string` | `us-east-1`   | no       |

## Outputs

| Name                       | Description                                   |
|----------------------------|-----------------------------------------------|
| `main_queue_url`           | The URL of the primary SQS queue.             |
| `dlq_url`                  | The URL of the Dead Letter Queue.             |
| `archive_bucket_name`      | The name of the S3 bucket for archiving.      |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Testing

Refer to the `tests/run_tests.sh` script for how to run the module's offline, deterministic tests.
