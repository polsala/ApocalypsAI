# Nightly Cloud-Whisperer Postbox

This Terraform module provisions a whimsical-yet-useful "Cloud-Whisperer Postbox" in AWS. It consists of a private S3 bucket configured to send notifications to an SNS topic whenever new objects (our "whispers") are created within it. This setup is ideal for triggering downstream processes, asynchronous communication between services, or simply logging new data arrivals.

## Features

*   **Secure Storage:** A private AWS S3 bucket for storing your digital whispers.
*   **Event-Driven Notifications:** Automatically publishes messages to an AWS SNS topic upon object creation in the S3 bucket.
*   **Configurable Filters:** Optionally filter notifications based on object key prefix or suffix.
*   **Whimsical Naming:** Default resource names reflect the ApocalypsAI theme.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "whisper_postbox" {
  source = "./path/to/nightly-cloud-whisperer-postbox" # Adjust path if used as a local module

  bucket_name_prefix = "my-secret-whispers"
  sns_topic_name     = "my-whisper-alerts"
  notification_filter_prefix = "inbox/"
  notification_filter_suffix = ".txt"
  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
  }
}

output "postbox_bucket_arn" {
  value = module.whisper_postbox.s3_bucket_arn
}

output "postbox_sns_topic_arn" {
  value = module.whisper_postbox.sns_topic_arn
}
```

## Inputs

| Name                       | Description                                                               | Type        | Default                               | Required |
|----------------------------|---------------------------------------------------------------------------|-------------|---------------------------------------|----------|
| `bucket_name_prefix`       | Prefix for the S3 bucket name. A unique suffix will be added.             | `string`    | `"apocalypsai-whisper-postbox-"`     | no       |
| `sns_topic_name`           | Name for the SNS topic.                                                   | `string`    | `"apocalypsai-whisper-channel"`       | no       |
| `notification_filter_prefix` | S3 object key prefix to filter notifications. Set to empty string for no prefix filter. | `string`    | `""`                                  | no       |
| `notification_filter_suffix` | S3 object key suffix to filter notifications. Set to empty string for no suffix filter. | `string`    | `""`                                  | no       |
| `tags`                     | A map of tags to assign to the resources.                                 | `map(string)` | `{}`                                  | no       |

## Outputs

| Name                | Description                 |
|---------------------|-----------------------------|
| `s3_bucket_id`      | The ID of the S3 bucket.    |
| `s3_bucket_arn`     | The ARN of the S3 bucket.   |
| `sns_topic_arn`     | The ARN of the SNS topic.   |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script. This script uses `terraform plan` to verify the module's configuration without deploying any actual cloud resources.

```bash
cd nightly-cloud-whisperer-postbox/tests
./test.sh
```
