# Nightly Cloud-Whisperer Beacon

## Overview

The `nightly-cloud-whisperer-beacon` is a whimsical-yet-useful Terraform module designed to provision a highly available, low-cost static website on AWS S3 and CloudFront. It serves as a digital beacon for broadcasting critical community messages, status updates, or whimsical musings across the digital wasteland.

This utility ensures your message reaches far and wide, secured with HTTPS and delivered efficiently via CloudFront's global network.

## Features

*   **Static Content Hosting**: Utilizes an AWS S3 bucket for storing your beacon's content.
*   **Global Delivery**: Leverages AWS CloudFront for content delivery, ensuring low latency and high availability worldwide.
*   **Secure Access**: Configures an Origin Access Control (OAC) for CloudFront to securely access the S3 bucket, preventing direct public access to the bucket.
*   **HTTPS Enabled**: CloudFront automatically provides HTTPS for your beacon's domain.
*   **Cost-Effective**: Designed for minimal operational costs, ideal for long-term, low-traffic messaging.

## Prerequisites

Before deploying the beacon, ensure you have the following:

1.  **AWS Account**: An active AWS account.
2.  **AWS CLI Configured**: The AWS Command Line Interface (CLI) installed and configured with credentials that have permissions to create S3 buckets, CloudFront distributions, and IAM policies.
3.  **Terraform Installed**: Terraform CLI (v1.0.0 or higher) installed on your local machine.

## Usage

1.  **Navigate to the module directory**:
    ```bash
    cd nightly-cloud-whisperer-beacon/src
    ```

2.  **Initialize Terraform**: This downloads the necessary AWS provider plugins.
    ```bash
    terraform init
    ```

3.  **Review the plan**: See what resources Terraform will create.
    ```bash
    terraform plan
    ```

4.  **Apply the configuration**: This will provision the AWS resources.
    ```bash
    terraform apply
    ```
    Type `yes` when prompted to confirm the deployment.

5.  **Access your beacon**: After `terraform apply` completes, the CloudFront domain name will be displayed in the outputs. Navigate to this URL in your web browser.

6.  **Destroy the beacon**: When the beacon is no longer needed, you can tear down all provisioned resources.
    ```bash
    terraform destroy
    ```
    Type `yes` when prompted to confirm the destruction.

## Inputs

| Name                 | Description                                                              | Type     | Default                 | Required |
| :------------------- | :----------------------------------------------------------------------- | :------- | :---------------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended.       | `string` | `"apocalypsai-beacon"` | no       |
| `region`             | The AWS region where the S3 bucket will be created.                      | `string` | `"us-east-1"`         | no       |
| `content_path`       | The local path to the directory containing the static website content.   | `string` | `"src/content"`       | no       |

## Outputs

| Name                     | Description                                      |
| :----------------------- | :----------------------------------------------- |
| `cloudfront_domain_name` | The domain name of the CloudFront distribution.  |
| `s3_bucket_id`           | The ID (name) of the S3 bucket created.          |

## Customization

To change the content of your beacon, simply modify the `index.html` file located in `src/content/index.html`. After making changes, run `terraform apply` again to upload the updated content to your S3 bucket and invalidate the CloudFront cache (if configured for invalidation, which is not explicitly done in this basic setup but CloudFront will eventually pick up changes).

For more advanced customization, you can modify `src/main.tf` to add custom domains, SSL certificates, or more complex CloudFront behaviors.
