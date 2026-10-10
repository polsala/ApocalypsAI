# Nightly Temporal Message Drop

A Terraform module to provision a secure, ephemeral message drop-off point in the AWS cloud. Perfect for leaving cryptic notes for future survivors, automated agents, or simply for temporary data exchange with a self-destruct timer.

## Features

*   **Secure:** Private S3 bucket with public access blocked.
*   **Ephemeral:** Configurable lifecycle rules to automatically delete messages after a set period.
*   **Versioned:** Keeps track of message changes, offering a rudimentary "temporal" history.
*   **Simple:** Easy to deploy and integrate into existing AWS infrastructure.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "temporal_message_drop" {
  source = "./nightly-temporal-message-drop" # Or a Git/S3 source in a real scenario

  bucket_name_prefix = "apocalypsai-messages-"
  message_retention_days = 7 # Messages will be deleted after 7 days
  tags = {
    Project = "ApocalypsAI"
    Purpose = "TemporalMessageDrop"
  }
}

output "message_drop_bucket_name" {
  value = module.temporal_message_drop.bucket_name
  description = "The name of the S3 bucket for temporal messages."
}

output "message_drop_bucket_arn" {
  value = module.temporal_message_drop.bucket_arn
  description = "The ARN of the S3 bucket for temporal messages."
}
```

## Requirements

*   Terraform CLI (v1.0.0+)
*   AWS Provider configured with appropriate credentials (for actual deployment)

## Inputs

| Name                     | Description                                     | Type     | Default | Required |
|--------------------------|-------------------------------------------------|----------|---------|----------|
| `bucket_name_prefix`     | A prefix for the S3 bucket name.                | `string` | `null`  | yes      |
| `message_retention_days` | Number of days after which messages are deleted.| `number` | `30`    | no       |
| `tags`                   | A map of tags to assign to the S3 bucket.       | `map`    | `{}`    | no       |

## Outputs

| Name                     | Description                                     |
|--------------------------|-------------------------------------------------|
| `bucket_name`            | The name of the created S3 bucket.              |
| `bucket_arn`             | The ARN of the created S3 bucket.               |
| `bucket_id`              | The ID of the created S3 bucket.                |
