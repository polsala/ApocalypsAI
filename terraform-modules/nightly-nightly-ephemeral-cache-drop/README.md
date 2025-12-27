# Nightly Ephemeral Cache Drop

A Terraform module to provision a self-cleaning, ephemeral AWS S3 bucket for temporary digital data drops. Perfect for sharing sensitive-but-temporary files, or as a quick-and-dirty backup location that automatically cleans itself up.

## Features

*   **Ephemeral by Design**: Objects automatically expire and are deleted after a configurable number of days (default: 7 days).
*   **Secure Defaults**: Private bucket, block public access, default server-side encryption (SSE-S3).
*   **Simple Integration**: Easily include in your existing Terraform configurations.

## Usage

To use this module, add it to your Terraform configuration:

```terraform
module "ephemeral_cache_drop" {
  source = "./nightly-ephemeral-cache-drop" # Or a Git/S3 source if published
  
  bucket_name_prefix = "my-secret-stash"
  expiration_days    = 3
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Ephemeral"
  }
}

output "cache_bucket_id" {
  description = "The ID of the ephemeral cache S3 bucket."
  value       = module.ephemeral_cache_drop.bucket_id
}

output "cache_bucket_arn" {
  description = "The ARN of the ephemeral cache S3 bucket."
  value       = module.ephemeral_cache_drop.bucket_arn
}
```

## Inputs

| Name               | Description                                     | Type          | Default                 | Required |
| :----------------- | :---------------------------------------------- | :------------ | :---------------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended. | `string`      | `"apocalypsai-cache"` | no       |
| `expiration_days`  | Number of days after which objects in the bucket will expire and be deleted. | `number`      | `7`                     | no       |
| `tags`             | A map of tags to assign to the S3 bucket.       | `map(string)` | `{}`                    | no       |

## Outputs

| Name           | Description                               |
| :------------- | :---------------------------------------- |
| `bucket_id`    | The ID (name) of the ephemeral cache S3 bucket. |
| `bucket_arn`   | The ARN of the ephemeral cache S3 bucket. |

## Testing

The module includes a self-contained test suite that validates the Terraform configuration without deploying actual resources.

To run the tests:

```bash
cd tests
./test.sh
```
