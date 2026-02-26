# Nightly Cloud Beacon

## Overview

The `nightly-cloud-beacon` is a whimsical-yet-useful Terraform module designed to provision a highly available static website on AWS. It leverages S3 for content storage and CloudFront for global content delivery and HTTPS, acting as a digital 'beacon' for the ApocalypsAI community. Use it to broadcast emergency messages, share community updates, or simply signal a friendly "we're still here!" across the digital wasteland.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for robust and scalable static content storage.
*   **Global Content Delivery**: Employs AWS CloudFront for low-latency content delivery, caching, and HTTPS support.
*   **Optional Custom Domain**: Integrates with AWS Route 53 to easily point a custom domain to your beacon.
*   **Whimsical Default Content**: Comes with a default `index.html` and `error.html` to get your beacon shining immediately.

## Prerequisites

*   An AWS account with appropriate permissions to create S3 buckets, CloudFront distributions, and (optionally) Route 53 records.
*   [Terraform CLI](https://www.terraform.io/downloads.html) installed (v1.6+ recommended for `terraform test`).
*   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

## Usage

1.  **Create a new Terraform configuration** in a directory outside this module (e.g., `my-beacon-deployment/`).

2.  **Define the module in your `main.tf`**: 

    ```terraform
    # my-beacon-deployment/main.tf
    module "community_beacon" {
      source = "./path/to/nightly-cloud-beacon/src" # Adjust path as necessary

      bucket_name = "apocalypsai-community-beacon-12345" # Must be globally unique
      # Optional: Uncomment and configure for a custom domain
      # domain_name = "beacon.yourdomain.com"
      # zone_id     = "YOUR_ROUTE53_HOSTED_ZONE_ID"
    }

    output "beacon_url" {
      description = "The URL of the deployed Cloud Beacon."
      value       = module.community_beacon.custom_domain_url != "N/A" ? module.community_beacon.custom_domain_url : module.community_beacon.cloudfront_url
    }
    ```

3.  **Initialize Terraform**: 

    ```bash
    terraform init
    ```

4.  **Review the plan**: 

    ```bash
    terraform plan
    ```

5.  **Apply the configuration**: 

    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

6.  **Access your beacon**: After the apply completes, Terraform will output the `beacon_url`. Navigate to this URL in your browser to see your Nightly Cloud Beacon in action!

## Inputs

| Name        | Description                                                                                             | Type   | Default | Required |
| :---------- | :------------------------------------------------------------------------------------------------------ | :----- | :------ | :------- |
| `bucket_name` | The name for the S3 bucket that will host the static website content. Must be globally unique.          | `string` | n/a     | yes      |
| `domain_name` | (Optional) The custom domain name to associate with the CloudFront distribution. Leave empty to use CloudFront's default domain. | `string` | `""`    | no       |
| `zone_id`     | (Optional) The Route 53 Hosted Zone ID for the custom domain. Required if `domain_name` is set.         | `string` | `""`    | no       |

## Outputs

| Name                   | Description                                      |
| :--------------------- | :----------------------------------------------- |
| `s3_bucket_name`       | The name of the S3 bucket.                       |
| `s3_website_endpoint`  | The S3 static website endpoint.                  |
| `cloudfront_domain_name` | The domain name of the CloudFront distribution.  |
| `cloudfront_url`       | The full HTTPS URL of the CloudFront distribution. |
| `custom_domain_url`    | The custom domain URL if configured, otherwise "N/A". |

## Testing

This module includes automated tests using `terraform test`. To run the tests:

```bash
cd nightly-cloud-beacon/tests
terraform test
```

The tests use a `mock_provider` to simulate AWS resources, ensuring they are deterministic and run offline without requiring actual AWS credentials or API calls.
