# Nightly Temporal Data Vault

A Terraform module to provision a secure, versioned, and lifecycle-managed AWS S3 bucket. This vault is designed to safely store your precious temporal data, ensuring data integrity through versioning and cost-effectiveness with lifecycle rules.

## Features

*   **Versioning Enabled**: Keeps a history of every object change, allowing for easy rollback and recovery from accidental deletions or overwrites.
*   **Server-Side Encryption**: All objects are encrypted at rest using AES256.
*   **Public Access Blocked**: By default, all public access to the bucket is blocked, adhering to security best practices.
*   **Lifecycle Management**: Configurable rules to automatically transition older object versions to cheaper storage classes (like S3 Standard-IA) or expire them after a specified period.
*   **Private by Default**: Access Control Lists (ACLs) are set to private.

## Usage

To use this module, include it in your Terraform configuration and provide the required inputs.

```terraform
module "my_temporal_vault" {
  source = "./path/to/nightly-temporal-data-vault/src" # Adjust path as needed

  bucket_name                        = "my-apocalypsai-data-vault-unique-name"
  enable_versioning                  = true
  enable_lifecycle_rules             = true
  noncurrent_version_expiration_days = 90  # Delete noncurrent versions after 90 days
  transition_current_to_ia_days      = 30  # Transition current versions to IA after 30 days
  transition_noncurrent_to_ia_days   = 60  # Transition noncurrent versions to IA after 60 days

  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Owner       = "NightlyIntegrator"
  }
}

output "vault_bucket_id" {
  value = module.my_temporal_vault.bucket_id
}

output "vault_bucket_arn" {
  value = module.my_temporal_vault.bucket_arn
}
```

## Inputs

| Name                               | Description                                                                                             | Type        | Default | Required |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------ | :---------- | :------ | :------- |
| `bucket_name`                      | The name of the S3 bucket to create.                                                                    | `string`    | n/a     | yes      |
| `enable_versioning`                | Whether to enable versioning for the S3 bucket.                                                         | `bool`      | `true`  | no       |
| `enable_lifecycle_rules`           | Whether to enable lifecycle rules for the S3 bucket.                                                    | `bool`      | `true`  | no       |
| `noncurrent_version_expiration_days` | Number of days after which noncurrent versions of objects will be permanently deleted.                  | `number`    | `90`    | no       |
| `transition_current_to_ia_days`    | Number of days after which current versions of objects will be transitioned to STANDARD_IA storage class. Set to `0` to disable. | `number`    | `30`    | no       |
| `transition_noncurrent_to_ia_days` | Number of days after which noncurrent versions of objects will be transitioned to STANDARD_IA storage class. Set to `0` to disable. | `number`    | `60`    | no       |
| `tags`                             | A map of tags to assign to the bucket.                                                                  | `map(string)` | `{}`    | no       |

## Outputs

| Name                          | Description                                 |
| :---------------------------- | :------------------------------------------ |
| `bucket_id`                   | The ID of the S3 bucket.                    |
| `bucket_arn`                  | The ARN of the S3 bucket.                   |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.  |

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script.

```bash
cd tests/
./test.sh
```

This script will perform `terraform init -backend=false`, `terraform validate`, and `terraform plan` against the test configurations, ensuring the module's syntax and structure are correct without deploying actual cloud resources.
