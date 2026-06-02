# Nightly Temporal Archive Vault

This Terraform module provisions an AWS S3 bucket specifically configured for long-term, secure, and versioned archival storage. It's designed to serve as a "digital time capsule" for critical data, historical records, or disaster recovery assets that need to persist through the ages.

## Features

*   **Secure**: Enforces server-side encryption (AES256) and blocks all public access.
*   **Versioned**: Keeps multiple versions of objects, protecting against accidental deletions or overwrites.
*   **Long-Term Archival**: Automatically transitions objects to cost-effective GLACIER_IR and DEEP_ARCHIVE storage classes.
*   **Configurable Expiration**: Optionally sets an expiration policy for objects.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_digital_time_capsule" {
  source = "./modules/nightly-temporal-archive-vault"

  bucket_name = "my-apocalypsai-time-capsule-unique-name-12345"
  region      = "us-east-1"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "DigitalTimeCapsule"
  }
  glacier_ir_transition_days = 30   # Transition to Glacier Instant Retrieval after 30 days
  deep_archive_transition_days = 90 # Transition to Deep Archive after 90 days
  expiration_days = null           # Objects never expire (set to a number for expiration)
}

output "time_capsule_bucket_id" {
  value = module.my_digital_time_capsule.bucket_id
}

output "time_capsule_bucket_arn" {
  value = module.my_digital_time_capsule.bucket_arn
}
```

## Inputs

| Name                           | Description                                                                 | Type        | Default     | Required |
| :----------------------------- | :-------------------------------------------------------------------------- | :---------- | :---------- | :------- |
| `bucket_name`                  | The name of the S3 bucket to create. Must be globally unique.               | `string`    | n/a         | yes      |
| `region`                       | The AWS region where the S3 bucket will be created.                         | `string`    | `"us-east-1"` | no       |
| `tags`                         | A map of tags to assign to the bucket.                                      | `map(string)` | `{}`        | no       |
| `glacier_ir_transition_days`   | Number of days after object creation to transition to GLACIER_IR storage class. | `number`    | `30`        | no       |
| `deep_archive_transition_days` | Number of days after object creation to transition to DEEP_ARCHIVE storage class. | `number`    | `90`        | no       |
| `expiration_days`              | Number of days after object creation to expire (delete) the object. Set to `null` for no expiration. | `number`    | `null`      | no       |

## Outputs

| Name                 | Description                               | Value |
| :------------------- | :---------------------------------------- | :---- |
| `bucket_id`          | The ID (name) of the S3 bucket.           | `string` |
| `bucket_arn`         | The ARN of the S3 bucket.                 | `string` |
| `bucket_domain_name` | The S3 bucket regional domain name.       | `string` |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
