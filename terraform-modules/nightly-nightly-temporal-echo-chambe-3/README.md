# Nightly Temporal Echo Chamber Vault

This Terraform module provisions an ephemeral AWS S3 bucket, designed for storing short-lived, sensitive data in a post-apocalyptic communication network. Data stored in this "Temporal Echo Chamber" is automatically purged after a configurable number of days, ensuring that whispers of the past don't linger too long.

## Features

*   **Ephemeral Storage**: Configurable lifecycle rule to automatically delete objects after a specified duration.
*   **Secure by Default**: Private bucket access with public access blocked.
*   **Customizable**: Easily set the bucket name prefix and expiration period.

## Usage

To deploy a Temporal Echo Chamber Vault, include this module in your Terraform configuration:

```terraform
module "echo_chamber_vault" {
  source = "./nightly-temporal-echo-chamber-vault/src" # Adjust path as needed
  
  bucket_name_prefix = "apocalypsai-echo-chamber"
  expiration_days    = 7 # Data will be purged after 7 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Wasteland"
  }
}

output "echo_chamber_bucket_id" {
  value       = module.echo_chamber_vault.bucket_id
  description = "The ID of the Temporal Echo Chamber S3 bucket."
}

output "echo_chamber_bucket_arn" {
  value       = module.echo_chamber_vault.bucket_arn
  description = "The ARN of the Temporal Echo Chamber S3 bucket."
}
```

## Module Inputs

| Name                 | Description                                     | Type   | Default     | Required |
| :------------------- | :---------------------------------------------- | :----- | :---------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be added. | `string` | `""`        | yes      |
| `expiration_days`    | Number of days after which objects will be automatically deleted. | `number` | `30`        | no       |
| `tags`               | A map of tags to assign to the bucket.          | `map(string)` | `{}`        | no       |
| `acl`                | The canned ACL to apply to the bucket.          | `string` | `"private"` | no       |

## Module Outputs

| Name                  | Description                                     |
| :-------------------- | :---------------------------------------------- |
| `bucket_id`           | The ID (name) of the S3 bucket.                 |
| `bucket_arn`          | The ARN of the S3 bucket.                       |
| `bucket_domain_name`  | The S3 bucket's domain name.                    |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
*   Configured AWS credentials (for actual deployment, not for testing)
