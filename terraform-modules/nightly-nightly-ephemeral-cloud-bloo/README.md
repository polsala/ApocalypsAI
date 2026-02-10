# Nightly Ephemeral Cloud Bloom

A whimsical-yet-useful Terraform module to provision an ephemeral AWS S3 bucket for temporary static content. This "digital garden" automatically "wilts" (deletes) its contents after a configurable period, encouraging experimentation without leaving permanent digital debris.

## Features

*   **Ephemeral Storage**: Provisions an S3 bucket with an automatic lifecycle policy to delete objects after a specified number of days.
*   **Configurable Wilting**: Easily set the `expiration_days` for your digital blooms.
*   **Optional Public Access**: Can be configured for public static website hosting for temporary demos or file sharing.
*   **Tagging**: Automatically tags resources for easy identification and management.

## Usage

To use this module, ensure you have Terraform installed and configured with AWS credentials.

### Example Configuration

```terraform
# main.tf
provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "my_ephemeral_bloom" {
  source = "./src" # Path to the module's src directory

  bucket_name_prefix = "my-daily-bloom"
  expiration_days    = 7 # Objects will be deleted after 7 days
  enable_public_access = true # Enable for static website hosting
  tags = {
    Project = "ApocalypsAI"
    Environment = "Ephemeral"
  }
}

output "bloom_bucket_url" {
  description = "The URL of the ephemeral S3 bucket (if public access enabled)."
  value       = module.my_ephemeral_bloom.bucket_website_endpoint
}

output "bloom_bucket_arn" {
  description = "The ARN of the ephemeral S3 bucket."
  value       = module.my_ephemeral_bloom.bucket_arn
}
```

### Deployment Steps

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```
2.  **Review the Plan**:
    ```bash
    terraform plan
    ```
3.  **Apply the Configuration**:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.
4.  **Upload Content (Optional)**:
    If `enable_public_access` is `true`, you can upload `index.html` and `error.html` to the created S3 bucket to host a static website.
    ```bash
    aws s3 cp ./index.html s3://$(terraform output -raw bloom_bucket_id)/index.html
    aws s3 cp ./error.html s3://$(terraform output -raw bloom_bucket_id)/error.html
    ```
5.  **Destroy Resources (Optional, but recommended for ephemeral blooms)**:
    When you're done, or if you want to manually "wilt" your garden before its natural expiration:
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## Module Inputs

| Name                 | Description                                                                                             | Type        | Default           | Required |
| :------------------- | :------------------------------------------------------------------------------------------------------ | :---------- | :---------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name to ensure uniqueness. The full name will be `<prefix>-ephemeral-cloud-bloom`. | `string`    | `"apocalypsai"`   | no       |
| `expiration_days`    | Number of days after which objects in the bucket will be automatically deleted (wilting period).          | `number`    | `30`              | no       |
| `enable_public_access` | Set to `true` to enable public access for static website hosting. WARNING: This makes your bucket content publicly readable. | `bool`      | `false`           | no       |
| `tags`               | A map of tags to assign to the S3 bucket.                                                               | `map(string)` | `{}`              | no       |

## Module Outputs

| Name                      | Description                                                               |
| :------------------------ | :------------------------------------------------------------------------ |
| `bucket_id`               | The ID (name) of the S3 bucket.                                           |
| `bucket_arn`              | The ARN of the S3 bucket.                                                 |
| `bucket_website_endpoint` | The S3 bucket website endpoint (if public access is enabled).             |
| `lifecycle_rule_id`       | The ID of the lifecycle rule applied to the bucket.                       |
| `lifecycle_expiration_days` | The number of days after which objects will expire.                       |

## Testing

This module includes `terraform test` configurations to validate its behavior without requiring actual resource provisioning.

To run the tests:

```bash
terraform test
```

These tests perform a `terraform plan` and assert on the module's outputs and computed resource attributes, ensuring the configuration is correctly generated according to the inputs.
