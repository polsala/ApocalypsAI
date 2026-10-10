# Nightly Cloud Beacon

A Terraform module designed to provision a resilient, low-cost static website "beacon" in AWS. This utility allows the community to deploy a simple, highly available digital presence, capable of broadcasting a message of hope, critical updates, or whimsical musings across the digital wasteland. It leverages AWS S3 for storage and CloudFront for global content delivery and HTTPS.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for robust and scalable static content storage.
*   **Global Content Delivery**: Employs AWS CloudFront CDN for low-latency access and DDoS protection.
*   **HTTPS Enabled**: CloudFront automatically provides HTTPS for secure communication.
*   **Cost-Effective**: Designed for minimal operational costs, ideal for a persistent, low-traffic beacon.
*   **Customizable Message**: Easily set the beacon's message via a Terraform variable.

## Usage

To deploy your own Nightly Cloud Beacon, you'll need AWS credentials configured for Terraform.

1.  **Create a `main.tf` file**:
    ```terraform
    module "nightly_beacon" {
      source = "./path/to/nightly-cloud-beacon/src" # Adjust path as necessary

      bucket_name_prefix = "apocalypsai-beacon" # Must be globally unique
      content_message    = "The stars still shine, even in the void. Stay strong, survivors!"
      aws_region         = "us-east-1" # Or your preferred AWS region
    }

    output "beacon_url" {
      value       = module.nightly_beacon.cloudfront_domain_name
      description = "The URL of your Nightly Cloud Beacon."
    }
    ```

2.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

3.  **Plan and Apply**:
    ```bash
    terraform plan
    terraform apply
    ```

After successful application, the `beacon_url` output will provide the URL to your deployed static website.

## Module Inputs

| Name                 | Description                                                               | Type     | Default     | Required |
| :------------------- | :------------------------------------------------------------------------ | :------- | :---------- | :------- |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. A random suffix will be added.    | `string` | `""`        | yes      |
| `content_message`    | The HTML content or message to display on the beacon's `index.html` page. | `string` | `"Hello, survivor!"` | no       |
| `aws_region`         | The AWS region where resources will be deployed.                          | `string` | `"us-east-1"` | no       |

## Module Outputs

| Name                       | Description                               |
| :------------------------- | :---------------------------------------- |
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution. |
| `s3_bucket_website_endpoint` | The S3 static website endpoint URL.       |
| `s3_bucket_id`             | The ID of the S3 bucket.                  |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables).
