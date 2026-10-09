# nightly-scavenger-cache-vault

A whimsical-yet-robust Terraform module designed to provision a secure, versioned, and lifecycle-managed AWS S3 bucket. Perfect for safeguarding your precious post-apocalyptic digital findings, rare data fragments, or the last known recipe for pre-collapse artisanal sourdough.

## Features

*   **Secure by Default**: Blocks public access and enables server-side encryption (SSE-S3).
*   **Versioned Storage**: Keeps track of every iteration of your findings, protecting against accidental deletions or overwrites.
*   **Lifecycle Management**: Automatically transitions older data to cheaper storage (Glacier) and eventually expires it, optimizing costs for your long-term digital hoard.
*   **Customizable**: Easily configure bucket name, region, tags, and lifecycle rules.

## Usage

To deploy your very own Scavenger Cache Vault, include this module in your Terraform configuration:

```terraform
module "my_scavenger_cache" {
  source = "./path/to/nightly-scavenger-cache-vault/src" # Adjust path as needed

  bucket_name = "my-precious-findings-vault-2024"
  region      = "us-east-1"
  tags = {
    Environment = "Wasteland"
    Owner       = "ApocalypsAI"
    Purpose     = "DigitalHoard"
  }

  enable_versioning                       = true
  enable_encryption                       = true
  lifecycle_rule_days_to_expire           = 180 # Expire objects after 180 days
  lifecycle_rule_days_to_transition_to_glacier = 60 # Transition to Glacier after 60 days
}

output "vault_id" {
  value = module.my_scavenger_cache.s3_bucket_id
}

output "vault_arn" {
  value = module.my_scavenger_cache.s3_bucket_arn
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the bucket.

## Inputs

| Name                                   | Description                                                               | Type   | Default | Required |
| :------------------------------------- | :------------------------------------------------------------------------ | :----- | :------ | :------- |
| `bucket_name`                          | The name of the S3 bucket. Must be globally unique.                       | `string` | n/a     | yes      |
| `region`                               | The AWS region where the bucket will be created.                          | `string` | n/a     | yes      |
| `tags`                                 | A map of tags to assign to the bucket.                                    | `map(string)` | `{}`    | no       |
| `enable_versioning`                    | Whether to enable versioning for the bucket.                              | `bool` | `true`  | no       |
| `enable_encryption`                    | Whether to enable default server-side encryption (SSE-S3) for the bucket. | `bool` | `true`  | no       |
| `lifecycle_rule_days_to_expire`        | Number of days after which noncurrent object versions will expire.        | `number` | `90`    | no       |
| `lifecycle_rule_days_to_transition_to_glacier` | Number of days after which noncurrent object versions will transition to GLACIER storage class. | `number` | `30`    | no       |

## Outputs

| Name                  | Description                               |
| :-------------------- | :---------------------------------------- |
| `s3_bucket_id`        | The ID (name) of the S3 bucket.           |
| `s3_bucket_arn`       | The ARN of the S3 bucket.                 |
| `s3_bucket_domain_name` | The domain name of the S3 bucket.       |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
