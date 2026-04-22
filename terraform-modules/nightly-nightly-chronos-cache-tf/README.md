# nightly-chronos-cache-tf

## "The Chronos Cache: Ephemeral Storage Blessed by Time"

This Terraform module provisions an AWS S3 bucket designed for temporary storage, automatically expiring its contents and itself after a configurable number of days. It's perfect for CI/CD artifacts, temporary data processing outputs, or any data that has a defined, short lifespan.

### Why use the Chronos Cache?

In the post-apocalyptic landscape, resources are precious. The Chronos Cache ensures that your temporary data doesn't linger, consuming valuable storage and incurring unnecessary costs. It's a self-cleaning solution for your transient digital needs, ensuring your infrastructure remains lean and efficient.

### Features

*   **Self-Expiring:** Configurable lifecycle rules automatically delete objects and non-current versions after a set duration.
*   **Secure by Default:** Public access is blocked to prevent accidental exposure.
*   **Versioning Enabled:** Supports object versioning to ensure lifecycle rules for non-current versions function correctly.
*   **Clean Cleanup:** Aborts incomplete multipart uploads to prevent orphaned data.

## Usage

To use the Chronos Cache, include the module in your Terraform configuration and provide the required variables.

```terraform
module "my_ephemeral_cache" {
  source = "./path/to/nightly-chronos-cache-tf/src" # Adjust path as needed

  bucket_name_prefix = "my-app-temp-data"
  expiration_days    = 14 # Data will expire after 14 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Development"
    Owner       = "IntegratorAgent"
  }
}

output "cache_bucket_name" {
  value       = module.my_ephemeral_cache.bucket_id
  description = "The name of the ephemeral S3 bucket."
}

output "cache_bucket_arn" {
  value       = module.my_ephemeral_cache.bucket_arn
  description = "The ARN of the ephemeral S3 bucket."
}
```

## Inputs

| Name               | Description                                                                 | Type     | Default | Required |
| :----------------- | :-------------------------------------------------------------------------- | :------- | :------ | :------- |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. Terraform will append a unique suffix. | `string` | n/a     | yes      |
| `expiration_days`  | Number of days after which objects (and non-current versions) in the bucket will be automatically deleted. | `number` | `7`     | no       |
| `tags`             | A map of tags to assign to the bucket.                                      | `map(string)` | `{}`    | no       |

## Outputs

| Name                        | Description                                     |
| :-------------------------- | :---------------------------------------------- |
| `bucket_id`                 | The name (ID) of the S3 bucket.                 |
| `bucket_arn`                | The ARN of the S3 bucket.                       |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.      |

## Testing

To ensure the module's integrity and functionality without provisioning actual cloud resources, run the provided `test.sh` script. This script performs `terraform init`, `terraform validate`, and `terraform plan` against a mock configuration.

```bash
cd nightly-chronos-cache-tf/tests
./test.sh
```

This will validate the Terraform syntax and generate a plan, confirming that the module is correctly structured and its variables are properly handled.
