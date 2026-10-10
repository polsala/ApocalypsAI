# Nightly Chronicle Archive Terraform Module

This Terraform module provisions a highly resilient, versioned, and encrypted object storage solution, ideal for safeguarding critical temporal data archives, survival logs, or historical records in a post-apocalyptic landscape.

## Features

*   **AWS S3 Bucket**: Core storage for your chronicles.
*   **Versioning Enabled**: Protects against accidental deletions and overwrites, allowing you to retrieve previous versions of your data.
*   **Server-Side Encryption (SSE-S3)**: Ensures your data is encrypted at rest by default.
*   **Public Access Blocked**: Secure by default, preventing unintended public exposure of your sensitive archives.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables. Ensure your AWS provider is configured.

```terraform
module "chronicle_archive" {
  source = "./src" # Or a remote source like a Git repository

  bucket_name = "my-apocalypsai-chronicles-unique-id"
  region      = "us-east-1"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "ChronicleArchive"
  }
}

output "archive_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = module.chronicle_archive.bucket_id
}

output "archive_bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = module.chronicle_archive.bucket_arn
}

output "archive_bucket_domain_name" {
  description = "The domain name of the S3 bucket."
  value       = module.chronicle_archive.bucket_domain_name
}
```

Replace `my-apocalypsai-chronicles-unique-id` with a globally unique identifier for your bucket name, as S3 bucket names must be unique across all AWS accounts.

## Inputs

| Name                        | Description                                                               | Type          | Default     | Required |
| :-------------------------- | :------------------------------------------------------------------------ | :------------ | :---------- | :------- |
| `bucket_name`               | The name of the S3 bucket to create. Must be globally unique.             | `string`      | `null`      | yes      |
| `region`                    | The AWS region where the S3 bucket will be created.                       | `string`      | `us-east-1` | no       |
| `tags`                      | A map of tags to assign to the S3 bucket.                                 | `map(string)` | `{}`        | no       |

## Outputs

| Name                       | Description                                   |
| :------------------------- | :-------------------------------------------- |
| `bucket_id`                | The ID (name) of the S3 bucket.               |
| `bucket_arn`               | The ARN of the S3 bucket.                     |
| `bucket_domain_name`       | The S3 bucket's regional domain name.         |

## Testing

To ensure the module's integrity and syntax, you can run the provided tests:

1.  Navigate to the `tests/` directory:
    ```bash
    cd tests/
    ```
2.  Run the test script:
    ```bash
    ./test.sh
    ```

This script will perform `terraform validate` on both the module source and the test configuration, and then generate a `terraform plan` without applying any changes. This verifies the HCL syntax and module's ability to generate a plan, which are offline operations. No actual AWS resources are created or modified during these tests.
