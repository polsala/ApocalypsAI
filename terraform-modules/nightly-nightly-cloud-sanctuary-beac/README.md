# Nightly Cloud Sanctuary Beacon

This Terraform module provisions a highly available, static website on AWS using S3 and CloudFront. It's designed to serve as a resilient, global communication beacon for the ApocalypsAI community, allowing for the dissemination of vital messages, safe haven coordinates, or whimsical affirmations in a post-apocalyptic landscape.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for cost-effective and scalable static content delivery.
*   **Global Reach & HTTPS**: Leverages AWS CloudFront for content delivery network (CDN) capabilities, ensuring low latency and secure (HTTPS) access worldwide.
*   **Simple Deployment**: Easily deployable with standard Terraform commands.
*   **Customizable Content**: Upload your own `index.html` or use the provided whimsical `beacon_message.html`.

## Prerequisites

*   An AWS Account with appropriate permissions to create S3 buckets, S3 bucket policies, and CloudFront distributions.
*   [Terraform CLI](https://www.terraform.io/downloads.html) installed (v1.0+ recommended).
*   AWS credentials configured for Terraform (e.g., via `~/.aws/credentials` or environment variables).

## Usage

1.  **Create a new Terraform configuration**: Create a directory for your beacon (e.g., `my-beacon`) and add a `main.tf` file.

    ```terraform
    # my-beacon/main.tf
    module "community_beacon" {
      source = "./path/to/nightly-cloud-sanctuary-beacon/src"

      # Required variables
      bucket_name_prefix = "apocalypsai-community-beacon"
      region             = "us-east-1"

      # Optional: specify a custom content file path relative to the module's root
      # content_file_path = "path/to/your/custom_index.html"
    }

    output "beacon_url" {
      description = "The URL of the CloudFront distribution for the beacon."
      value       = module.community_beacon.cloudfront_domain_name
    }

    output "s3_website_endpoint" {
      description = "The S3 static website endpoint (without CloudFront)."
      value       = module.community_beacon.s3_bucket_website_endpoint
    }
    ```

2.  **Initialize Terraform**: Navigate to your `my-beacon` directory and run:

    ```bash
    terraform init
    ```

3.  **Review the plan**: See what resources Terraform will create:

    ```bash
    terraform plan
    ```

4.  **Apply the configuration**: Deploy your beacon to AWS:

    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

5.  **Access your beacon**: After a few minutes (CloudFront distribution takes time to deploy), use the `beacon_url` output to access your static website.

    ```bash
    terraform output beacon_url
    ```

## Module Inputs

| Name                 | Description                                                               | Type     | Default                      | Required |
| :------------------- | :------------------------------------------------------------------------ | :------- | :--------------------------- | :------- |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. A random suffix will be added.    | `string` | `"apocalypsai-beacon"`      | yes      |
| `content_file_path`  | Path to the HTML file to upload as the beacon's content.                  | `string` | `"beacon_message.html"`      | no       |
| `region`             | The AWS region where the S3 bucket and CloudFront distribution will be created. | `string` | `"us-east-1"`                | no       |

## Module Outputs

| Name                         | Description                                            |
| :--------------------------- | :----------------------------------------------------- |
| `cloudfront_domain_name`     | The domain name of the AWS CloudFront distribution.    |
| `s3_bucket_website_endpoint` | The S3 static website endpoint (without CloudFront).   |

## Testing

To ensure the module's syntax and configuration are valid without deploying resources, you can use the following commands from the module's root directory (`nightly-cloud-sanctuary-beacon/src`):

```bash
terraform init
terraform validate
terraform plan
```

The `tests/main.tf` file provides a minimal example of how to instantiate the module, which is used by `terraform validate` to check for correct variable usage and resource definitions. This ensures the module is syntactically correct and adheres to Terraform's HCL (HashiCorp Configuration Language) rules.
