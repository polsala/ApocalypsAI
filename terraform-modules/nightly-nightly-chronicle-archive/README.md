# Nightly Chronicle Archive

This Terraform module provisions a highly resilient and versioned AWS S3 bucket, designed to serve as a "Chronicle Archive" for preserving critical data, historical records, or vital knowledge fragments in a post-apocalyptic scenario.

It ensures data integrity and availability through:
- **Versioning:** Keeps a complete history of all object changes.
- **Server-Side Encryption:** Encrypts data at rest using AES256.
- **Public Access Block:** Prevents accidental or intentional public exposure.
- **Lifecycle Management (Optional):** Automatically transitions older versions to more cost-effective storage (e.g., Glacier) or expires them after a defined period.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "chronicle_archive" {
  source = "./path/to/nightly-chronicle-archive" # Adjust path as necessary

  bucket_name                      = "my-apocalypsai-chronicles-unique-name"
  environment                      = "production"
  enable_lifecycle_rules           = true
  noncurrent_version_transition_days = 90
  noncurrent_version_expiration_days = 365
}

output "archive_bucket_id" {
  value = module.chronicle_archive.bucket_id
}

output "archive_bucket_arn" {
  value = module.chronicle_archive.bucket_arn
}
```

## Inputs

| Name                               | Description                                                                 | Type     | Default   | Required |
|------------------------------------|-----------------------------------------------------------------------------|----------|-----------|----------|
| `bucket_name`                      | The name of the S3 bucket for the chronicle archive.                        | `string` | n/a       | yes      |
| `environment`                      | The environment tag for the bucket.                                         | `string` | `"production"` | no       |
| `enable_lifecycle_rules`           | Whether to enable lifecycle rules for archiving old versions.               | `bool`   | `true`    | no       |
| `noncurrent_version_transition_days` | Number of days after which noncurrent versions transition to GLACIER.       | `number` | `90`      | no       |
| `noncurrent_version_expiration_days` | Number of days after which noncurrent versions expire.                      | `number` | `365`     | no       |

## Outputs

| Name           | Description                     |
|----------------|---------------------------------|
| `bucket_id`    | The ID of the S3 bucket.        |
| `bucket_arn`   | The ARN of the S3 bucket.       |

## Requirements

- Terraform 0.13+
- AWS Provider configured with appropriate credentials.

## Testing

To run the module's tests, navigate to the `tests/` directory and execute `terraform test`.

```bash
cd tests
terraform init
terraform test
```
