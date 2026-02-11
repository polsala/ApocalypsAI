# Nightly Temporal Beacon Emitter

This Terraform module provisions a secure, versioned AWS S3 bucket designed to act as a 'temporal beacon' within your cloud infrastructure. In the ApocalypsAI universe, this beacon helps mark stable zones or resource caches across the temporal fabric. In practical terms, it provides a robust, low-cost, and easily identifiable storage endpoint for various operational needs.

## Features

*   **Secure**: Enforces server-side encryption (SSE-S3) and blocks public access.
*   **Reliable**: Enables bucket versioning to protect against accidental deletions or overwrites.
*   **Identifiable**: Automatically tags the bucket with `Name`, `Environment`, and `ManagedBy` for easy tracking.
*   **Configurable**: Allows customization of the bucket name prefix, AWS region, and environment.

## Usage

To deploy a temporal beacon, include this module in your Terraform configuration:

1.  **Create a `main.tf` file** (e.g., in a new directory `my-beacon-deployment/`):

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired region
    }

    module "temporal_beacon" {
      source = "./path/to/nightly-temporal-beacon-emitter/src" # Adjust path as needed

      bucket_name_prefix = "my-apocalypsai-safezone"
      region             = "us-east-1" # Must match provider region for consistency
      environment        = "production"
    }

    output "beacon_bucket_id" {
      description = "The ID of the deployed temporal beacon S3 bucket."
      value       = module.temporal_beacon.bucket_id
    }

    output "beacon_bucket_arn" {
      description = "The ARN of the deployed temporal beacon S3 bucket."
      value       = module.temporal_beacon.bucket_arn
    }
    ```

2.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

3.  **Review the plan**:

    ```bash
    terraform plan
    ```

4.  **Apply the changes**:

    ```bash
    terraform apply
    ```

## Inputs

| Name                 | Description                                       | Type     | Default                 | Required |
| :------------------- | :------------------------------------------------ | :------- | :---------------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended. | `string` | `apocalypsai-beacon`   | no       |
| `region`             | The AWS region where the S3 bucket will be created. | `string` | `us-east-1`             | no       |
| `environment`        | The environment tag for the S3 bucket.            | `string` | `dev`                   | no       |

## Outputs

| Name                 | Description                                       | Value                                   |
| :------------------- | :------------------------------------------------ | :-------------------------------------- |
| `bucket_id`          | The ID (name) of the S3 bucket.                   | `aws_s3_bucket.temporal_beacon.id`      |
| `bucket_arn`         | The ARN of the S3 bucket.                         | `aws_s3_bucket.temporal_beacon.arn`     |
| `bucket_domain_name` | The domain name of the S3 bucket.                 | `aws_s3_bucket.temporal_beacon.bucket_domain_name` |
