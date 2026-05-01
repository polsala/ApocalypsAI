# Nightly Scavenger Cache Vault

This Terraform module provisions a highly durable, low-cost, and secure AWS S3 bucket, designed to serve as a "scavenger's cache" for vital digital information in a post-apocalyptic landscape. It's ideal for storing backups of critical data, survival plans, logs, or precious digital memories with resilience and cost-efficiency.

## Features

*   **S3 Bucket**: Creates a new AWS S3 bucket.
*   **Versioning**: Automatically enables object versioning to protect against accidental deletions or overwrites.
*   **Encryption**: Enforces server-side encryption (SSE-S3) for all objects at rest.
*   **Public Access Block**: Configures the bucket to block all public access, ensuring data privacy.
*   **Lifecycle Rules**: Implements a lifecycle rule to transition objects to the `GLACIER` storage class after a configurable number of days, optimizing storage costs.
*   **Optional Access Logging**: Can be configured to send access logs to another S3 bucket for auditing.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_survival_cache" {
  source = "./path/to/nightly-scavenger-cache-vault/src"

  bucket_name             = "apocalypsai-survival-data-cache-prod"
  environment             = "production"
  glacier_transition_days = 60 # Move to Glacier after 60 days
  tags = {
    Project     = "ApocalypsAI"
    Owner       = "IntegratorAgent"
    Sensitivity = "High"
  }
  # Uncomment the line below to enable access logging
  # access_logging_bucket_name = ["apocalypsai-log-archive-bucket"]
}

output "cache_bucket_arn" {
  value = module.my_survival_cache.s3_bucket_arn
}
```

## Inputs

| Name                         | Description                                                                                             | Type          | Default       | Required |
| :--------------------------- | :------------------------------------------------------------------------------------------------------ | :------------ | :------------ | :------- |
| `bucket_name`                | The name of the S3 bucket to create. Must be globally unique.                                           | `string`      | n/a           | yes      |
| `environment`                | The environment tag for the bucket (e.g., 'prod', 'dev', 'wasteland').                                  | `string`      | `"wasteland"` | no       |
| `tags`                       | A map of tags to assign to the bucket.                                                                  | `map(string)` | `{}`          | no       |
| `glacier_transition_days`    | Number of days after which to transition objects to GLACIER storage class.                              | `number`      | `30`          | no       |
| `access_logging_bucket_name` | Optional: The name of the S3 bucket where access logs should be stored. If `null`, logging is disabled. | `list(string)`| `null`        | no       |

## Outputs

| Name                  | Description                       |
| :-------------------- | :--------------------------------|
| `s3_bucket_id`        | The ID of the S3 bucket.          |
| `s3_bucket_arn`       | The ARN of the S3 bucket.         |
| `s3_bucket_domain_name` | The S3 bucket domain name.        |
