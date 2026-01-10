# Nightly Ephemeral Echo Vault

This Terraform module provisions an AWS S3 bucket designed for temporary storage, automatically self-destructing its contents and the bucket itself after a specified 'temporal decay' period. It's ideal for ephemeral data drops, temporary testing environments, or any scenario where data needs to vanish without a trace after a set time.

## Features

*   **Ephemeral Storage**: Creates an S3 bucket with a lifecycle rule to expire all objects and then delete the bucket itself.
*   **Configurable Decay**: The self-destruction period (in days) is easily configurable.
*   **Secure by Default**: Uses AWS S3's native lifecycle management for reliable deletion.

## Usage

To use this module, include it in your root Terraform configuration and provide the necessary variables.

### Example `main.tf`

```terraform
provider "aws" {
  region = "us-east-1" # Or your desired AWS region
}

module "echo_vault" {
  source = "./src" # Path to this module's 'src' directory

  bucket_name_prefix = "my-secret-temporal-drop"
  region             = "us-east-1" # Must match provider region
  decay_period_days  = 3           # Bucket and contents self-destruct after 3 days
}

output "vault_bucket_id" {
  description = "The ID of the ephemeral echo vault S3 bucket."
  value       = module.echo_vault.bucket_id
}

output "vault_bucket_arn" {
  description = "The ARN of the ephemeral echo vault S3 bucket."
  value       = module.echo_vault.bucket_arn
}
```

### Variables

| Name               | Description                                                               | Type   | Default | Required |
|--------------------|---------------------------------------------------------------------------|--------|---------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. The module will append a random suffix. | `string` | n/a     | yes      |
| `region`           | The AWS region where the S3 bucket will be created.                       | `string` | n/a     | yes      |
| `decay_period_days`| Number of days after which the bucket and its contents will be automatically deleted. | `number` | `7`     | no       |

## Deployment

1.  **Initialize Terraform**: `terraform init`
2.  **Review Plan**: `terraform plan`
3.  **Apply Changes**: `terraform apply`

Remember to clean up resources if they are no longer needed before the decay period, or simply let the temporal decay take its course!
