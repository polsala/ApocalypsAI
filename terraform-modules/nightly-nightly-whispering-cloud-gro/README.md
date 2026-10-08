# Nightly Whispering Cloud Grove

This Terraform module provisions a serverless static website on AWS, utilizing S3 for content storage and CloudFront for global content delivery and caching. It's designed to host a "Whispering Cloud Grove" – a simple, low-cost platform for displaying daily generated messages, affirmations, or whimsical tidbits.

## Features

*   **Static Website Hosting**: Secure and scalable content delivery via AWS S3.
*   **Global CDN**: Low-latency content access and caching with AWS CloudFront.
*   **Cost-Effective**: Pay-as-you-go, serverless architecture.
*   **Customizable**: Easily integrate your own content generation or deployment pipeline.

## Usage

To deploy your own Whispering Cloud Grove, you'll need an AWS account and Terraform installed.

1.  **Configure AWS Credentials**: Ensure your AWS CLI or environment variables are configured with appropriate credentials.
2.  **Create a `main.tf` file**:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your preferred region
    }

    module "whispering_grove" {
      source = "./nightly-whispering-cloud-grove" # Adjust path if not in root
      
      # Optional: Provide a unique prefix for your S3 bucket name
      bucket_name_prefix = "my-whisper-grove" 
      
      # Optional: Set to true to enable S3 bucket versioning
      enable_s3_versioning = true
    }

    output "cloudfront_domain_name" {
      description = "The domain name of the CloudFront distribution."
      value       = module.whispering_grove.cloudfront_domain_name
    }

    output "s3_bucket_website_endpoint" {
      description = "The S3 bucket website endpoint (for direct access, not recommended for production)."
      value       = module.whispering_grove.s3_bucket_website_endpoint
    }
    ```

3.  **Initialize Terraform**:
    ```bash
    terraform init
    ```
4.  **Review the Plan**:
    ```bash
    terraform plan
    ```
5.  **Apply the Configuration**:
    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

After successful application, the `cloudfront_domain_name` output will provide the URL for your Whispering Cloud Grove. You can then upload your static `index.html` (or other content) to the S3 bucket created by this module.

## Inputs

| Name                     | Description                                                               | Type     | Default     | Required |
| :----------------------- | :------------------------------------------------------------------------ | :------- | :---------- | :------- |
| `bucket_name_prefix`     | A unique prefix for the S3 bucket name. A random suffix will be added.    | `string` | `"whispers"` | no       |
| `enable_s3_versioning`   | Whether to enable versioning on the S3 bucket.                            | `bool`   | `false`     | no       |
| `index_document`         | The name of the index document (e.g., `index.html`).                      | `string` | `"index.html"` | no       |
| `error_document`         | The name of the error document (e.g., `error.html`).                      | `string` | `"error.html"` | no       |

## Outputs

| Name                       | Description                                         |
| :------------------------- | :-------------------------------------------------- |
| `s3_bucket_id`             | The ID of the S3 bucket.                            |
| `s3_bucket_arn`            | The ARN of the S3 bucket.                           |
| `s3_bucket_website_endpoint` | The S3 bucket website endpoint.                   |
| `cloudfront_distribution_id` | The ID of the CloudFront distribution.            |
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution.     |
| `cloudfront_hosted_zone_id`| The CloudFront hosted zone ID.                      |

## Development & Testing

This module includes a basic test setup to validate its configuration.

1.  Navigate to the `tests/` directory:
    ```bash
    cd tests
    ```
2.  Initialize Terraform for the test configuration:
    ```bash
    terraform init
    ```
3.  Run the test script:
    ```bash
    ./test.sh
    ```

The `test.sh` script will run `terraform validate` and `terraform plan` to ensure the module's syntax is correct and a plan can be generated without errors. It does not provision actual AWS resources.
