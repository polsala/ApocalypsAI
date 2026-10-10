# Nightly Chronos Cache

A whimsical-yet-useful Terraform module for provisioning an AWS S3 bucket configured as a "Chronos Cache" – a temporal echo chamber for your data. This module ensures your data is versioned, creating echoes of its past states, and automatically manages older versions to balance resilience with storage costs.

## Features

*   **Temporal Echoes**: Automatically enables S3 Versioning to keep a history of all changes to your objects.
*   **Echo Decay**: Configurable lifecycle rules to transition noncurrent (older) versions to cheaper storage classes (e.g., S3 Standard-IA, Glacier) and eventually expire them, preventing infinite storage growth while retaining historical echoes.
*   **Secure by Default**: Applies a public access block to ensure the bucket is not publicly accessible.
*   **Customizable**: Easily configure bucket name, ACL, and echo retention policies.

## Usage

To deploy your own Chronos Cache, create a `main.tf` file in your Terraform project:

```terraform
module "my_chronos_cache" {
  source = "./path/to/nightly-chronos-cache/src" # Adjust path as needed

  bucket_name = "my-apocalypsai-chronos-cache-unique-name" # IMPORTANT: Must be globally unique!
  bucket_acl  = "private" # Recommended for security
  noncurrent_transition_days = 45 # Transition noncurrent versions to IA after 45 days
  noncurrent_expiration_days = 180 # Expire noncurrent versions after 180 days
  tags = {
    Project     = "ApocalypsAI-Survival"
    Environment = "Production"
  }
}

output "cache_bucket_arn" {
  value = module.my_chronos_cache.bucket_arn
}
```

Then, run the standard Terraform commands:

```bash
terraform init
terraform plan
terraform apply
```

## Module Inputs

| Name                                | Description                                                               | Type        | Default       | Required |
| :---------------------------------- | :------------------------------------------------------------------------ | :---------- | :------------ | :------- |
| `bucket_name`                       | The name of the S3 bucket to create. Must be globally unique.             | `string`    | n/a           | yes      |
| `bucket_acl`                        | The ACL to apply to the bucket. Recommended: 'private'.                   | `string`    | `"private"`   | no       |
| `noncurrent_transition_days`        | Number of days after which noncurrent versions transition to a different storage class. | `number` | `30`          | no       |
| `noncurrent_transition_storage_class` | The storage class to transition noncurrent versions to (e.g., GLACIER, STANDARD_IA). | `string` | `"STANDARD_IA"` | no       |
| `noncurrent_expiration_days`        | Number of days after which noncurrent versions expire and are permanently deleted. | `number` | `90`          | no       |
| `tags`                              | A map of tags to assign to the bucket.                                    | `map(string)` | `{}`          | no       |
| `aws_region`                        | The AWS region to deploy the S3 bucket in.                                | `string`    | `"us-east-1"` | no       |

## Module Outputs

| Name               | Description                               |
| :----------------- | :---------------------------------------- |
| `bucket_id`        | The ID of the S3 bucket.                  |
| `bucket_arn`       | The ARN of the S3 bucket.                 |
| `bucket_domain_name` | The S3 bucket regional domain name.       |

## Testing

The module includes a test configuration in the `tests/` directory. To validate the module's syntax and variable definitions offline:

```bash
cd tests
terraform init
terraform validate
```

This will check the HCL syntax and ensure all required variables are provided to the module without attempting to provision any actual cloud resources.
