# Nightly Digital Time Capsule

A Terraform module designed to provision a secure, versioned, and lifecycle-managed AWS S3 bucket. This utility is perfect for storing important digital artifacts, messages for the future, or critical data that needs to be preserved and potentially archived over time, acting as a 'digital time capsule'.

## Features

*   **Secure**: Blocks all public access and enforces server-side encryption (SSE-S3) by default.
*   **Versioned**: Keeps multiple versions of objects, protecting against accidental deletions or overwrites.
*   **Lifecycle Managed**: Optionally configures rules to transition older versions to more cost-effective storage classes (like Glacier) and eventually prune them.
*   **Whimsical**: Named 'Digital Time Capsule' to encourage thoughtful preservation of digital heritage in an uncertain future.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_time_capsule" {
  source = "./path/to/nightly-digital-time-capsule/src" # Adjust path as needed

  bucket_name_prefix = "my-apocalypsai-capsule" # Required: A unique prefix for your bucket name
  tags = {
    Environment = "production"
    Project     = "ApocalypsAI"
    Owner       = "Community"
  }
  
  # Optional: Enable and configure lifecycle rules
  enable_lifecycle_rules       = true
  lifecycle_rule_days_to_glacier = 365 # Transition non-current versions to Glacier after 365 days
  lifecycle_rule_days_to_delete  = 730 # Delete non-current versions and expired object delete markers after 730 days
}
```

## Inputs

| Name                         | Description                                                                 | Type     | Default     | Required |
|------------------------------|-----------------------------------------------------------------------------|----------|-------------|----------|
| `bucket_name_prefix`         | A unique prefix for the S3 bucket name. The module will append a random string. | `string` | n/a         | yes      |
| `tags`                       | A map of tags to apply to the S3 bucket.                                    | `map`    | `{}`        | no       |
| `enable_lifecycle_rules`     | Whether to enable lifecycle rules for the bucket.                           | `bool`   | `false`     | no       |
| `lifecycle_rule_days_to_glacier` | Number of days after which non-current versions transition to GLACIER_IR. | `number` | `365`       | no       |
| `lifecycle_rule_days_to_delete`  | Number of days after which non-current versions and expired object delete markers are permanently deleted. | `number` | `730`       | no       |

## Outputs

| Name          | Description                                 |
|---------------|---------------------------------------------|
| `bucket_id`   | The ID of the S3 bucket.                    |
| `bucket_arn`  | The ARN of the S3 bucket.                   |
| `bucket_name` | The full generated name of the S3 bucket.   |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`

## Testing

Refer to the `tests/test.sh` script for how to run local, offline validation and plan checks.
