# Nightly Chrono-Vault

A whimsical yet practical Terraform module for creating an AWS S3 bucket with automated lifecycle management. Perfect for data that needs to undergo "temporal stasis" (transition to colder storage) before its eventual "entropic decay" (deletion).

## Features

*   **Configurable Bucket Naming**: Define a unique name for your Chrono-Vault.
*   **Automated Temporal Stasis**: Automatically transition objects to the cost-effective AWS GLACIER storage class after a specified number of days.
*   **Optional Entropic Decay**: Configure an optional period after which objects will be permanently deleted, ensuring data hygiene and compliance.
*   **Versioning Enabled**: Automatically enables versioning on the bucket to protect against accidental overwrites or deletions.
*   **Whimsical Parameter Names**: Adds a touch of ApocalypsAI charm to your infrastructure-as-code.

## Usage

To use the Nightly Chrono-Vault, include the module in your Terraform configuration:

```terraform
module "my_precious_data_vault" {
  source = "./path/to/nightly-chrono-vault/src"

  bucket_name          = "my-apocalypsai-data-archive-2024"
  temporal_stasis_days = 90  # Move to GLACIER after 90 days
  entropic_decay_days  = 365 # Delete permanently after 365 days (from object creation)

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    DataTier    = "Archive"
  }
}

module "ephemeral_logs_vault" {
  source = "./path/to/nightly-chrono-vault/src"

  bucket_name          = "apocalypsai-ephemeral-logs"
  temporal_stasis_days = 7   # Move to GLACIER after 7 days
  entropic_decay_days  = 30  # Delete permanently after 30 days
}

module "indefinite_stasis_vault" {
  source = "./path/to/nightly-chrono-vault/src"

  bucket_name          = "apocalypsai-long-term-backup"
  temporal_stasis_days = 180 # Move to GLACIER after 180 days
  entropic_decay_days  = null # Keep in GLACIER indefinitely
}

output "precious_vault_arn" {
  value = module.my_precious_data_vault.bucket_arn
}
```

### Inputs

| Name                   | Description                                                                                                                              | Type    | Default | Required |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :------ | :------ | :------- |
| `bucket_name`          | The unique name for your S3 Chrono-Vault bucket.                                                                                         | `string`| n/a     | yes      |
| `temporal_stasis_days` | Number of days after which objects in the Chrono-Vault will enter 'temporal stasis' (transition to GLACIER storage class).                 | `number`| `30`    | no       |
| `entropic_decay_days`  | Optional: Number of days after which objects in the Chrono-Vault will undergo 'entropic decay' (permanent deletion). If `null`, objects will remain in GLACIER indefinitely. | `number`| `null`  | no       |
| `tags`                 | A map of tags to assign to the Chrono-Vault bucket.                                                                                      | `map(string)`| `{}`    | no       |

### Outputs

| Name        | Description                               | Value |
| :---------- | :---------------------------------------- | :---- |
| `bucket_id` | The ID of the S3 Chrono-Vault bucket.     | `string` |
| `bucket_arn`| The ARN of the S3 Chrono-Vault bucket.    | `string` |

## Requirements

*   [Terraform](https://www.terraform.io/downloads.html) (v1.0.0+)
*   [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest) (v4.0.0+)
*   Configured AWS credentials (e.g., via environment variables, AWS CLI, or IAM roles).

## Testing

To ensure the module is syntactically correct and adheres to Terraform best practices, run the provided test script:

```bash
./tests/test_module.sh
```

This script will perform `terraform fmt --check` and `terraform validate` on a test configuration that consumes the module, ensuring its integrity without provisioning actual cloud resources.
