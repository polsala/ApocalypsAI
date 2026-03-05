# Nightly Temporal Archive Vault

In these uncertain times, ensure your digital echoes resonate through the ages. The `nightly-temporal-archive-vault` Terraform module provides a robust, secure, and optionally immutable AWS S3 bucket, perfect for preserving critical data, historical records, or even your most cherished memes for future generations (or just long-term compliance).

## Features

*   **Secure Storage**: Provisions a private AWS S3 bucket.
*   **Versioning**: Automatically keeps multiple versions of your objects, protecting against accidental deletions or overwrites.
*   **Object Lock (Optional)**: Enables WORM (Write Once, Read Many) protection, making objects immutable for a specified retention period, ideal for compliance or critical archives.
*   **Public Access Block**: Configures the bucket to block all public access by default, enhancing security.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary inputs.

```terraform
module "my_temporal_archive" {
  source = "./path/to/nightly-temporal-archive-vault/src"

  bucket_name         = "my-community-archive-2024-alpha" # Must be globally unique
  region              = "us-east-1"
  enable_versioning   = true
  enable_object_lock  = true
  retention_mode      = "COMPLIANCE" # or "GOVERNANCE"
  retention_period_days = 365
}

output "archive_bucket_name" {
  value = module.my_temporal_archive.bucket_id
}

output "archive_bucket_arn" {
  value = module.my_temporal_archive.bucket_arn
}
```

### Inputs

| Name                  | Description                                                                                             | Type     | Default      | Required |
| :-------------------- | :------------------------------------------------------------------------------------------------------ | :------- | :----------- | :------- |
| `bucket_name`         | The name of the S3 bucket to create for the archive vault. Must be globally unique.                     | `string` | n/a          | yes      |
| `region`              | The AWS region where the S3 bucket will be created.                                                     | `string` | `"us-east-1"`| no       |
| `enable_versioning`   | Whether to enable versioning for the S3 bucket.                                                         | `bool`   | `true`       | no       |
| `enable_object_lock`  | Whether to enable S3 Object Lock for immutability. This must be set at bucket creation.                 | `bool`   | `false`      | no       |
| `retention_mode`      | The S3 Object Lock retention mode (`GOVERNANCE` or `COMPLIANCE`). Required if `enable_object_lock` is `true`. | `string` | `"GOVERNANCE"` | no       |
| `retention_period_days` | The number of days for S3 Object Lock retention. Required if `enable_object_lock` is `true`.          | `number` | `30`         | no       |

### Outputs

| Name                          | Description                                 |
| :---------------------------- | :------------------------------------------ |
| `bucket_id`                   | The ID (name) of the S3 bucket.             |
| `bucket_arn`                  | The ARN of the S3 bucket.                   |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.  |

## Testing

To validate the module's syntax and structure without deploying any resources, navigate to the `tests/` directory and run the provided `test.sh` script.

```bash
cd nightly-temporal-archive-vault/tests
./test.sh
```

This script performs `terraform init` (which may require network access to download providers) and `terraform validate` to ensure the module's HCL is correctly formed and adheres to best practices. It does not require AWS credentials for the `validate` step itself, making it suitable for offline syntax checks.
