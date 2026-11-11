# Nightly Ephemeral Vault

This Terraform module provisions an AWS S3 bucket designed for ephemeral data storage. It automatically configures a lifecycle policy to expire objects after a specified number of days, ensuring that temporary data is cleaned up without manual intervention.

It's perfect for temporary logs, transient build artifacts, short-lived message queues, or any data that needs to "self-destruct" after a set period.

## Features

*   **Ephemeral Storage**: Objects are automatically expired after a configurable duration.
*   **Secure by Default**: Private bucket access.
*   **Customizable Naming**: Define a prefix for your bucket name.
*   **Region Agnostic**: Deployable in any AWS region.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "ephemeral_vault" {
  source = "./nightly-ephemeral-vault/src" # Adjust path if not in root
  
  bucket_name_prefix = "my-temp-data"
  retention_days     = 7 # Objects will expire after 7 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
  }
}

output "ephemeral_vault_bucket_id" {
  description = "The ID of the ephemeral S3 bucket."
  value       = module.ephemeral_vault.bucket_id
}

output "ephemeral_vault_bucket_arn" {
  description = "The ARN of the ephemeral S3 bucket."
  value       = module.ephemeral_vault.bucket_arn
}
```

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_bucket_name_prefix"></a> [bucket\_name\_prefix](#input\_bucket\_name\_prefix) | A prefix for the S3 bucket name. A unique suffix will be appended. | `string` | n/a | yes |
| <a name="input_retention_days"></a> [retention\_days](#input\_retention\_days) | The number of days after which objects in the bucket will expire. | `number` | `30` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to assign to the S3 bucket. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_bucket_arn"></a> [bucket\_arn](#output\_bucket\_arn) | The ARN of the S3 bucket. |
| <a name="output_bucket_id"></a> [bucket\_id](#output\_bucket\_id) | The ID (name) of the S3 bucket. |

## Development

To run tests:
```bash
cd tests
./test.sh
```
