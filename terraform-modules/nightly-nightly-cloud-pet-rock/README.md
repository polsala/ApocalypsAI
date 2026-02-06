# Nightly Cloud Pet Rock

A whimsical-yet-useful Terraform module to deploy a minimal, always-on AWS S3 bucket, serving as a digital 'pet rock' for your cloud infrastructure.

## Summary

This module provisions an AWS S3 bucket, which can optionally be configured for static website hosting. It's designed to be a low-cost, persistent cloud resource that you can 'keep' as a digital companion, or use as a simple, tangible example for learning Terraform and AWS S3.

## Whimsical Use Cases

*   **Digital Companion**: A tiny, always-on presence in your cloud, a comforting thought in the vast digital wasteland.
*   **Terraform Playground**: A safe, isolated, and low-cost resource to experiment with Terraform deployments and lifecycle management.
*   **Static Content Host**: If `enable_website_hosting` is set to `true`, you can upload a simple `index.html` (perhaps an image of a pet rock!) and host it directly from your bucket.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables. The module will create an S3 bucket with a unique name based on the `bucket_name_prefix`.

### Example `main.tf`

```terraform
provider "aws" {
  region = "us-east-1"
}

module "my_cloud_pet_rock" {
  source               = "./modules/nightly-cloud-pet-rock" # Adjust path as needed
  bucket_name_prefix   = "my-first-pet-rock"
  enable_website_hosting = true
  aws_region           = "us-east-1"
}

output "pet_rock_url" {
  description = "The URL of your Cloud Pet Rock (if website hosting is enabled)."
  value       = module.my_cloud_pet_rock.website_endpoint
}
```

### Inputs

| Name                   | Description                                                                 | Type    | Default                     | Required |
| :--------------------- | :-------------------------------------------------------------------------- | :------ | :-------------------------- | :------- |
| `bucket_name_prefix`   | A unique prefix for the S3 bucket name. A random suffix will be appended.   | `string`| `"apocalypsai-pet-rock"` | no       |
| `enable_website_hosting` | Set to `true` to enable static website hosting for the S3 bucket.           | `bool`  | `false`                     | no       |
| `aws_region`           | The AWS region to deploy the S3 bucket in.                                  | `string`| `"us-east-1"`             | no       |

### Outputs

| Name             | Description                                                                 |
| :--------------- | :-------------------------------------------------------------------------- |
| `bucket_id`      | The ID of the S3 bucket.                                                    |
| `bucket_arn`     | The ARN of the S3 bucket.                                                   |
| `website_endpoint` | The website endpoint of the S3 bucket if website hosting is enabled.        |

## Testing

The module includes a self-contained test suite that uses `terraform plan` to validate the module's behavior without requiring actual AWS credentials or deployments.

To run the tests:

1.  Navigate to the `tests/` directory:
    ```bash
    cd tests
    ```
2.  Execute the test script:
    ```bash
    ./test.sh
    ```

The `test.sh` script will initialize Terraform and run `terraform plan` for various scenarios, checking the output for expected resource creations and configurations. It uses mock AWS credentials for `terraform plan` to ensure determinism and offline execution.
