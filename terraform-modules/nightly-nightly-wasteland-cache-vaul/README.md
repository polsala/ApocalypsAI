# Nightly Wasteland Cache Vault

This Terraform module provisions a secure, versioned AWS S3 bucket designed to safely store vital "wasteland resources." It incorporates best practices for data integrity and cost-effective long-term storage, mimicking resource management in a post-apocalyptic setting.

## Features

*   **Versioning:** Keeps a complete history of all objects, protecting against accidental deletions or overwrites.
*   **Server-Side Encryption:** All data is encrypted at rest using AES256.
*   **Lifecycle Management:** Configurable rules to automatically transition objects to cheaper storage classes (STANDARD_IA, GLACIER) and eventually expire them, optimizing storage costs while ensuring data retention.

## Usage

To use this module, include it in your Terraform configuration and provide the required inputs.

```terraform
module "wasteland_cache_vault" {
  source = "./path/to/nightly-wasteland-cache-vault/src"

  bucket_name = "my-apocalypsai-resource-cache"
  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Purpose     = "WastelandResourceStorage"
  }
  retention_days_standard_to_ia    = 45  # Move to Infrequent Access after 45 days
  retention_days_ia_to_glacier     = 120 # Move to Glacier after 120 days (from object creation)
  retention_days_glacier_to_delete = 730 # Delete after 730 days (from object creation)
}

output "cache_vault_url" {
  description = "The regional domain name of the S3 bucket."
  value       = module.wasteland_cache_vault.bucket_regional_domain_name
}
```

## Inputs

| Name                               | Description                                                                    | Type        | Default | Required |
| :--------------------------------- | :----------------------------------------------------------------------------- | :---------- | :------ | :------- |
| `bucket_name`                      | The name of the S3 bucket for the wasteland cache vault.                       | `string`    | n/a     | yes      |
| `tags`                             | A map of tags to assign to the bucket.                                         | `map(string)` | `{}`    | no       |
| `retention_days_standard_to_ia`    | Number of days after which objects in STANDARD storage class are moved to STANDARD_IA. | `number`    | `30`    | no       |
| `retention_days_ia_to_glacier`     | Number of days after which objects in STANDARD_IA storage class are moved to GLACIER.  | `number`    | `90`    | no       |
| `retention_days_glacier_to_delete` | Number of days after which objects in GLACIER storage class are permanently deleted.   | `number`    | `365`   | no       |

## Outputs

| Name                          | Description                                   |
| :---------------------------- | :-------------------------------------------- |
| `bucket_id`                   | The ID of the S3 bucket.                      |
| `bucket_arn`                  | The ARN of the S3 bucket.                     |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.    |
