# Nightly Reality Anchor Vault

The ApocalypsAI Nightly Integrator presents the "Reality Anchor Vault" – a robust Terraform module designed to deploy a highly available, immutable cloud storage solution. In an era of temporal anomalies and digital decay, safeguarding critical information is paramount. This vault ensures your essential data, from survival manifests to historical records, remains untainted and accessible, anchored firmly in reality.

## Features

*   **Immutable Storage**: Utilizes AWS S3 Object Lock in compliance mode to prevent accidental or malicious deletion/overwriting of objects for a specified retention period.
*   **Versioning**: Keeps a complete history of all object versions, allowing recovery from unintended changes.
*   **High Availability**: Leverages AWS S3's inherent multi-AZ architecture for maximum resilience.
*   **Encryption**: Encrypts data at rest by default using S3-managed keys (SSE-S3).
*   **Public Access Block**: Enforces strict public access blocking to prevent unintended data exposure.
*   **Whimsical Resilience**: Designed to withstand even the most mischievous temporal distortions, ensuring your data's integrity across fluctuating timelines.

## Usage

To deploy your own Reality Anchor Vault, ensure you have Terraform installed and AWS credentials configured.

```terraform
module "reality_anchor_vault" {
  source = "./nightly-reality-anchor-vault" # Or a Git/S3 source if published
  
  bucket_name      = "my-critical-data-anchor-vault"
  environment      = "production"
  retention_days   = 365 # Data will be immutable for 365 days
  tags = {
    Project = "ApocalypsAI"
    Purpose = "RealityAnchor"
  }
}

output "vault_bucket_arn" {
  description = "The ARN of the Reality Anchor Vault S3 bucket."
  value       = module.reality_anchor_vault.bucket_arn
}

output "vault_bucket_id" {
  description = "The ID of the Reality Anchor Vault S3 bucket."
  value       = module.reality_anchor_vault.bucket_id
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the vault.

## Inputs

| Name             | Description                                                               | Type          | Default | Required |
| :--------------- | :------------------------------------------------------------------------ | :------------ | :------ | :------- |
| `bucket_name`    | The name for the S3 bucket. Must be globally unique.                      | `string`      | `null`  | yes      |
| `environment`    | The environment (e.g., `dev`, `staging`, `production`). Used for tagging. | `string`      | `"dev"` | no       |
| `retention_days` | Number of days objects in the vault should be immutable (Object Lock in COMPLIANCE mode). | `number` | `365`   | no       |
| `tags`           | A map of tags to assign to the bucket.                                    | `map(string)` | `{}`    | no       |

## Outputs

| Name               | Description                                |
| :----------------- | :----------------------------------------- |
| `bucket_arn`       | The ARN of the S3 bucket.                  |
| `bucket_id`        | The ID (name) of the S3 bucket.            |
| `bucket_domain_name` | The S3 bucket's regional domain name.    |

## Requirements

| Name      | Version |
| :-------- | :------ |
| terraform | `>= 1.0` |
| aws       | `>= 4.0` |

## Contributing

Contributions are welcome! Please ensure your changes adhere to Terraform best practices and include comprehensive tests.
