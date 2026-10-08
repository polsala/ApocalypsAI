# Nightly Temporal Data Vault

A whimsical-yet-robust Terraform module for provisioning an AWS S3 bucket configured as a "Temporal Data Vault." This vault ensures your precious data is stored securely, versioned against accidental changes, and cost-optimized for long-term archival using intelligent lifecycle management.

## Features

*   **Versioned Storage:** Keeps multiple versions of an object, protecting against accidental deletions or overwrites.
*   **Server-Side Encryption:** Data at rest is encrypted by default using AWS S3-managed keys (SSE-S3).
*   **Lifecycle Management:** Automatically transitions older data versions to cheaper storage classes (e.g., Glacier) and eventually expires them, optimizing storage costs over time.
*   **Access Logging:** Optionally enables logging of all requests to the vault for auditing and security analysis.
*   **Tagging:** Applies standard tags for resource identification and cost allocation.

## Usage

To deploy your own Temporal Data Vault, include this module in your Terraform configuration:

```terraform
module "temporal_data_vault" {
  source = "./path/to/nightly-temporal-data-vault/src" # Adjust path as needed

  bucket_name          = "my-precious-temporal-vault-data"
  environment          = "production"
  project              = "ApocalypsAI"
  retention_days_to_glacier = 30  # Transition noncurrent versions to Glacier after 30 days
  expiration_days_noncurrent = 90 # Expire noncurrent versions after 90 days
  enable_access_logging = true
  logging_bucket_name   = "my-s3-access-logs-bucket" # Required if enable_access_logging is true
}
```

### Requirements

*   Terraform CLI (v1.0.0+)
*   AWS Provider configured with appropriate credentials and region.

## Inputs

| Name                        | Description                                                                 | Type     | Default    | Required |
| :-------------------------- | :-------------------------------------------------------------------------- | :------- | :--------- | :------- |
| `bucket_name`               | The name for the S3 bucket (must be globally unique).                       | `string` | `""`       | yes      |
| `environment`               | Environment tag for the bucket (e.g., `dev`, `prod`).                       | `string` | `"dev"`    | no       |
| `project`                   | Project tag for the bucket.                                                 | `string` | `"default"`| no       |
| `retention_days_to_glacier` | Number of days after which noncurrent versions transition to GLACIER.       | `number` | `30`       | no       |
| `expiration_days_noncurrent`| Number of days after which noncurrent versions are permanently deleted.     | `number` | `90`       | no       |
| `enable_access_logging`     | Whether to enable S3 access logging for the bucket.                         | `bool`   | `false`    | no       |
| `logging_bucket_name`       | The name of the S3 bucket where access logs will be stored. Required if `enable_access_logging` is `true`. | `string` | `null`     | no       |

## Outputs

| Name          | Description                                 |
| :------------ | :------------------------------------------ |
| `bucket_id`   | The ID (name) of the S3 bucket.             |
| `bucket_arn`  | The ARN of the S3 bucket.                   |
| `bucket_domain_name` | The S3 bucket's domain name.           |

## Testing

The module includes a basic test suite that uses `terraform validate` and `terraform plan` to ensure the module's syntax and configuration are correct without provisioning actual resources.

To run tests:

```bash
cd tests
./test.sh
```
