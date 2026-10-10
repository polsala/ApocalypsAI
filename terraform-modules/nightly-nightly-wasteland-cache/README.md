# Nightly Wasteland Resource Cache

A Terraform module to provision a highly secure and resilient AWS S3 bucket, perfect for storing vital post-apocalyptic resources. This module ensures your critical data is protected with features like versioning, server-side encryption, and comprehensive public access blocking.

## Features

*   **Secure Storage**: Creates a private S3 bucket.
*   **Versioning**: Automatically keeps multiple versions of your objects, protecting against accidental deletions or overwrites.
*   **Server-Side Encryption**: Encrypts all objects at rest using AES256.
*   **Public Access Blocking**: Prevents any public access to the bucket and its objects.
*   **Customizable**: Allows for custom bucket names and tags.

## Usage

To use this module, include it in your root Terraform configuration and provide the required variables.

```terraform
module "wasteland_cache" {
  source = "./path/to/nightly-wasteland-cache/src" # Adjust path as needed

  bucket_name                = "my-critical-wasteland-data-cache"
  region                     = "us-east-1" # Or your desired AWS region
  enable_versioning          = true
  enable_encryption          = true
  enable_public_access_block = true
  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Owner       = "SurvivorCollective"
  }
}

output "cache_bucket_id" {
  value = module.wasteland_cache.s3_bucket_id
}

output "cache_bucket_arn" {
  value = module.wasteland_cache.s3_bucket_arn
}
```

## Inputs

| Name                       | Description                                                     | Type        | Default       | Required |
| :------------------------- | :-------------------------------------------------------------- | :---------- | :------------ | :------- |
| `bucket_name`              | The name of the S3 bucket.                                      | `string`    | n/a           | yes      |
| `region`                   | The AWS region to deploy the S3 bucket in.                      | `string`    | `"us-east-1"` | no       |
| `enable_versioning`        | Whether to enable versioning for the S3 bucket.                 | `bool`      | `true`        | no       |
| `enable_encryption`        | Whether to enable default server-side encryption (AES256) for the S3 bucket. | `bool`      | `true`        | no       |
| `enable_public_access_block` | Whether to enable public access block settings for the S3 bucket. | `bool`      | `true`        | no       |
| `tags`                     | A map of tags to assign to the S3 bucket.                       | `map(string)` | `{}`          | no       |

## Outputs

| Name                    | Description                                |
| :---------------------- | :----------------------------------------- |
| `s3_bucket_id`          | The ID of the S3 bucket.                   |
| `s3_bucket_arn`         | The ARN of the S3 bucket.                  |
| `s3_bucket_domain_name` | The domain name of the S3 bucket.          |

## Requirements

This module requires the AWS provider to be configured with appropriate credentials to create S3 resources.
