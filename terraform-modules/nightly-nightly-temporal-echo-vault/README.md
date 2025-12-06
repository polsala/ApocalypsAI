# Nightly Temporal Echo Vault

A Terraform module designed to create an AWS S3 bucket configured as a "Temporal Echo Vault." This vault is not just for storage; it's for preserving data with a touch of temporal decay, simulating how information might fade or shift over time in an apocalyptic setting.

It sets up an S3 bucket with versioning and lifecycle rules to automatically transition objects to cheaper storage classes (like S3 Intelligent-Tiering or Glacier) and eventually expire them, creating a digital echo of their past existence.

## Features

*   **S3 Bucket Creation**: A dedicated S3 bucket for your temporal echoes.
*   **Versioning**: Keeps multiple versions of objects, allowing you to retrieve older "echoes."
*   **Lifecycle Rules**: Configurable rules to:
    *   Transition current object versions to S3 Intelligent-Tiering after a specified number of days.
    *   Transition non-current object versions to S3 Glacier after a specified number of days.
    *   Expire non-current object versions after a specified number of days, simulating data decay.
    *   Optionally expire current object versions after a very long period.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_echo_vault" {
  source = "./path/to/nightly-temporal-echo-vault/src"

  bucket_name_prefix = "my-apocalypse-data"
  region             = "us-east-1"
  echo_chamber_retention_days = 30  # Transition to Intelligent-Tiering after 30 days
  echo_chamber_glacier_days   = 90  # Transition non-current to Glacier after 90 days
  echo_chamber_decay_days     = 365 # Expire non-current versions after 365 days
  enable_versioning           = true
}

output "echo_vault_bucket_id" {
  value = module.my_echo_vault.bucket_id
  description = "The ID of the created S3 bucket."
}

output "echo_vault_bucket_arn" {
  value = module.my_echo_vault.bucket_arn
  description = "The ARN of the created S3 bucket."
}
```

### Inputs

| Name                          | Description                                                               | Type    | Default | Required |
| :---------------------------- | :------------------------------------------------------------------------ | :------ | :------ | :------- |
| `bucket_name_prefix`          | A prefix for the S3 bucket name. A unique suffix will be added.           | `string`| `null`  | yes      |
| `region`                      | The AWS region where the S3 bucket will be created.                       | `string`| `null`  | yes      |
| `echo_chamber_retention_days` | Number of days before current object versions transition to Intelligent-Tiering. | `number`| `30`    | no       |
| `echo_chamber_glacier_days`   | Number of days before non-current object versions transition to Glacier.  | `number`| `90`    | no       |
| `echo_chamber_decay_days`     | Number of days before non-current object versions are permanently deleted. | `number`| `365`   | no       |
| `enable_versioning`           | Whether to enable versioning on the S3 bucket.                            | `bool`  | `true`  | no       |

### Outputs

| Name                  | Description                               |
| :-------------------- | :---------------------------------------- |
| `bucket_id`           | The ID (name) of the created S3 bucket.   |
| `bucket_arn`          | The ARN of the created S3 bucket.         |

## Development & Testing

This module uses `terraform` for infrastructure definition.

### Prerequisites

*   Terraform CLI installed.

### Running Tests

The tests for this module are designed to be deterministic and offline. They validate the HCL syntax, formatting, and the presence of key configuration elements without requiring AWS credentials or network access.

```bash
cd tests
./test.sh
```

The `test.sh` script performs the following checks:
1.  `terraform validate`: Ensures the HCL syntax is correct and variables are properly used.
2.  `terraform fmt -check`: Verifies consistent code formatting.
3.  **Mocked Configuration Check**: It then statically analyzes the `main.tf` to ensure that the `aws_s3_bucket_lifecycle_configuration` and `aws_s3_bucket_versioning` resources are defined with the expected properties, simulating the outcome of a `terraform plan` without actual execution.
