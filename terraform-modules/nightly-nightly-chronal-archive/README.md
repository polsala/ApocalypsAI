# Nightly Chronal Archive

## A Terraform Module for Temporal Data Preservation

In the ever-shifting sands of the post-apocalyptic timeline, data integrity is paramount. The `Nightly Chronal Archive` is a whimsical-yet-robust Terraform module designed to provision a highly durable, versioned cloud storage bucket. Think of it as a digital time capsule, meticulously preserving "echoes" of your critical data across various temporal shifts and deployment cycles. Never again lose a precious byte to a rogue temporal anomaly or an accidental `rm -rf`!

This module creates an AWS S3 bucket configured for maximum data resilience, including versioning, server-side encryption, and public access blocking. It's your personal vault for historical data, configuration snapshots, or even the last known good state of reality itself.

## Features

*   **Temporal Versioning**: Automatically keeps multiple versions of your objects, allowing you to rewind to any previous "timeline."
*   **Echo Encryption**: Data is encrypted at rest, safeguarding your echoes from prying eyes and temporal snoopers.
*   **Anomaly-Resistant Access**: Blocks all public access by default, ensuring your archive remains a private sanctuary.
*   **Whimsical Tagging**: Automatically applies `apocalypsai` tags for easy identification in the vast cloud wasteland.

## Usage

To integrate the `Nightly Chronal Archive` into your infrastructure, simply include the module in your Terraform configuration.

```terraform
module "chronal_archive" {
  source = "./modules/nightly-chronal-archive" # Adjust path if not local

  bucket_name_prefix = "my-critical-data"
  environment        = "production-timeline-alpha"
  versioning_enabled = true
  tags = {
    Project = "ApocalypsAI"
    Purpose = "Chronal Archiving"
  }
}

output "archive_bucket_name" {
  description = "The name of the Chronal Archive S3 bucket."
  value       = module.chronal_archive.bucket_id
}

output "archive_bucket_arn" {
  description = "The ARN of the Chronal Archive S3 bucket."
  value       = module.chronal_archive.bucket_arn
}
```

### Inputs

| Name                 | Description                                                                 | Type    | Default                               | Required |
| :------------------- | :-------------------------------------------------------------------------- | :------ | :------------------------------------ | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. The module will append a unique suffix.    | `string`| `"apocalypsai-chronal-archive"`       | no       |
| `environment`        | The environment tag for the bucket (e.g., `dev`, `prod`, `test-timeline`).  | `string`| `"dev"`                               | no       |
| `versioning_enabled` | Whether to enable object versioning for the bucket.                         | `bool`  | `true`                                | no       |
| `tags`               | A map of tags to assign to the bucket.                                      | `map(string)` | `{}`                                  | no       |

### Outputs

| Name                 | Description                                     |
| :------------------- | :---------------------------------------------- |
| `bucket_id`          | The ID (name) of the S3 bucket.                 |
| `bucket_arn`         | The ARN of the S3 bucket.                       |
| `bucket_domain_name` | The domain name of the S3 bucket.               |

## Testing

This module is tested offline using `terraform validate` to ensure syntax correctness and proper variable definitions.

To run the tests:

1.  Navigate to the `tests/` directory.
2.  Run `./run_tests.sh`.

A successful validation indicates the module is syntactically sound and ready to preserve your temporal echoes.
