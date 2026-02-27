# Nightly Cloud-Gazer's Observatory

A whimsical yet robust Terraform module for deploying a secure, versioned AWS S3 bucket. Perfect for collecting and archiving your most precious "celestial anomaly" data, logs, or small files from the post-apocalyptic digital wasteland.

## Features

*   **Secure Storage**: All data is encrypted at rest using AES256 server-side encryption.
*   **Anomaly Tracking**: Versioning is enabled to keep a full history of all changes to your celestial observations.
*   **Cosmic Secrecy**: Public access is strictly blocked to prevent accidental exposure of your cosmic secrets.
*   **Ancient Prophecy Archival**: Optionally configure lifecycle rules to automatically transition older, less frequently accessed data to AWS Glacier for long-term, cost-effective archival.

## Usage

To deploy your own Cloud-Gazer's Observatory, include this module in your Terraform configuration:

```terraform
module "my_observatory" {
  source = "./path/to/nightly-cloud-gazer-observatory/src"

  bucket_name_prefix = "my-celestial-anomalies"
  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Owner       = "StargazerUnit"
  }

  # Optional: Enable archiving old data to Glacier
  enable_glacier_archive  = true
  glacier_archive_days    = 90  # Archive objects older than 90 days
  glacier_expiration_days = 3650 # Delete archived objects after 10 years
}

output "observatory_bucket_name" {
  value = module.my_observatory.bucket_id
}

output "observatory_bucket_arn" {
  value = module.my_observatory.bucket_arn
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision your observatory.

## Inputs

| Name                    | Description                                                                 | Type        | Default     | Required |
|:------------------------|:----------------------------------------------------------------------------|:------------|:------------|:---------|
| `bucket_name_prefix`    | A unique prefix for the S3 bucket name. Terraform will append a random string. | `string`    | n/a         | yes      |
| `tags`                  | A map of tags to assign to the S3 bucket.                                   | `map(string)` | `{}`        | no       |
| `enable_glacier_archive`| Set to `true` to enable a lifecycle rule to archive old data to Glacier.    | `bool`      | `false`     | no       |
| `glacier_archive_days`  | Number of days after which to transition objects to GLACIER storage class.  | `number`    | `90`        | no       |
| `glacier_expiration_days`| Number of days after which to permanently delete objects from GLACIER.      | `number`    | `3650`      | no       |

## Outputs

| Name                          | Description                                     |
|:------------------------------|:------------------------------------------------|
| `bucket_id`                   | The ID (name) of the S3 bucket.                 |
| `bucket_arn`                  | The ARN of the S3 bucket.                       |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.      |
