# Nightly Digital Time Capsule

A Terraform module to provision a highly durable and long-term storage solution in AWS S3, configured as a "Digital Time Capsule." This module sets up an S3 bucket with versioning, immutable object locking, and a lifecycle policy to ensure your precious digital artifacts are preserved for future generations (or at least for a very, very long time).

## Features

*   **S3 Bucket Creation**: A new S3 bucket with a unique name.
*   **Versioning Enabled**: Keeps a history of all object changes, allowing recovery from accidental deletions or overwrites.
*   **Immutable Object Lock**: Configured in `GOVERNANCE` mode with a customizable retention period (defaulting to 100 years), preventing objects from being deleted or overwritten until the retention period expires.
*   **Long-Term Lifecycle Policy**: Automatically transitions objects to cost-effective archival storage (e.g., Glacier Instant Retrieval) after a period, and optionally expires them after an even longer period.
*   **Encryption**: Server-side encryption (SSE-S3) enabled by default.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_time_capsule" {
  source  = "./terraform-modules/nightly-digital-time-capsule/src"
  bucket_name_prefix = "apocalypsai-capsule"
  retention_years    = 100 # Default, but can be overridden
  tags = {
    Project = "ApocalypsAI"
    Purpose = "DigitalTimeCapsule"
  }
}

output "time_capsule_bucket_name" {
  description = "The name of the created S3 bucket."
  value       = module.my_time_capsule.bucket_name
}

output "time_capsule_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = module.my_time_capsule.bucket_arn
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | `>= 1.0` |
| aws | `>= 4.0` |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended. | `string` | n/a | yes |
| `retention_years` | The number of years for object lock retention and lifecycle expiration. | `number` | `100` | no |
| `tags` | A map of tags to assign to the bucket. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | The name of the created S3 bucket. |
| `bucket_arn` | The ARN of the created S3 bucket. |
| `bucket_id` | The ID of the created S3 bucket. |

## Development

To run tests, navigate to the `tests/` directory within the module and execute `test.sh`.

```bash
cd terraform-modules/nightly-digital-time-capsule/tests
./test.sh
```
