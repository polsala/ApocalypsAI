# Nightly Whispering Log Archive

A Terraform module to provision a time-limited AWS S3 bucket for ephemeral logs or temporary data. This "Whispering Walls" archive ensures that data automatically fades away after a configurable retention period, perfect for temporary storage, testing environments, or compliance with short-term data policies.

## Features

*   **Ephemeral Storage**: Automatically purges objects after a specified number of days using S3 lifecycle rules.
*   **Secure by Default**: Blocks public access to the bucket.
*   **Customizable**: Easily configure bucket name, retention period, and tags.
*   **Simple Integration**: Designed as a reusable Terraform module.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "whispering_log_archive" {
  source = "./modules/nightly-whispering-log-archive" # Adjust path if not local
  
  bucket_name    = "my-ephemeral-logs-bucket"
  retention_days = 14 # Data will be deleted after 14 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
  }
}

output "archive_bucket_arn" {
  description = "The ARN of the Whispering Log Archive S3 bucket."
  value       = module.whispering_log_archive.bucket_arn
}
```

### Inputs

| Name             | Description                                     | Type          | Default                               | Required |
| :--------------- | :---------------------------------------------- | :------------ | :------------------------------------ | :------- |
| `bucket_name`    | The name of the S3 bucket.                      | `string`      | `"whispering-log-archive-<random_hex>"` | no       |
| `retention_days` | Number of days after which objects will expire. | `number`      | `7`                                   | no       |
| `tags`           | A map of tags to assign to the bucket.          | `map(string)` | `{}`                                  | no       |

### Outputs

| Name               | Description                                   |
| :----------------- | :-------------------------------------------- |
| `bucket_id`        | The ID of the S3 bucket.                      |
| `bucket_arn`       | The ARN of the S3 bucket.                     |
| `bucket_domain_name` | The domain name of the S3 bucket.             |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   An AWS account with configured credentials (for actual deployment, not for tests).

## Development & Testing

The module includes automated tests that validate its configuration using `terraform plan`. These tests require `terraform` and `jq` to be installed.

```bash
# From the module root directory (e.g., utils/nightly-whispering-log-archive)
./tests/test_module.sh
```
