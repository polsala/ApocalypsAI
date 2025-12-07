# Nightly Cloud Cache Keeper

This Terraform module provisions a robust, secure, and cost-effective AWS S3 bucket designed for storing critical "apocalyptic" data caches. It ensures data integrity and availability through versioning, server-side encryption, and lifecycle management rules.

## Features

*   **Versioned Storage**: Keeps multiple versions of objects, protecting against accidental deletions or overwrites.
*   **Encrypted by Default**: All objects are encrypted at rest using AES256 server-side encryption.
*   **Lifecycle Management**: Automatically transitions older data to cheaper storage classes (Glacier) and eventually expires it.
*   **Public Access Blocked**: Ensures the bucket is private and not publicly accessible.
*   **Customizable**: Allows configuration of bucket name, versioning, lifecycle durations, and tags.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "apocalypsai_cache" {
  source = "./path/to/nightly-cloud-cache-keeper/src"

  bucket_name                = "my-apocalypsai-data-cache"
  enable_versioning          = true
  transition_to_glacier_days = 45
  expire_after_days          = 365 * 5 # Keep data for 5 years
  environment                = "production"
  tags = {
    Project = "ApocalypsAI"
    Owner   = "IntegratorAgent"
  }
}

output "cache_bucket_name" {
  value = module.apocalypsai_cache.bucket_id
}

output "cache_bucket_arn" {
  value = module.apocalypsai_cache.bucket_arn
}
```

## Inputs

| Name                       | Description                                                              | Type      | Default       | Required |
| :------------------------- | :----------------------------------------------------------------------- | :-------- | :------------ | :------- |
| `bucket_name`              | The name of the S3 bucket to create.                                     | `string`  | n/a           | yes      |
| `enable_versioning`        | Whether to enable versioning on the S3 bucket.                           | `bool`    | `true`        | no       |
| `transition_to_glacier_days` | Number of days after which to transition objects to GLACIER storage class. | `number`  | `30`          | no       |
| `expire_after_days`        | Number of days after which to expire objects (delete them).              | `number`  | `365`         | no       |
| `environment`              | The environment tag for the bucket (e.g., 'dev', 'prod', 'wasteland').   | `string`  | `"wasteland"` | no       |
| `tags`                     | A map of additional tags to apply to the bucket.                         | `map(string)` | `{}`          | no       |

## Outputs

| Name                 | Description                               | Value |
| :------------------- | :---------------------------------------- | :---- |
| `bucket_id`          | The ID of the created S3 bucket.          | `string` |
| `bucket_arn`         | The ARN of the created S3 bucket.         | `string` |
| `bucket_domain_name` | The S3 bucket regional domain name.       | `string` |
