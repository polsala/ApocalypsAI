# Nightly Cloud Beacon

A Terraform module to deploy a simple, highly available static web beacon on AWS, displaying a customizable message for community communication.

## Overview

In the post-apocalyptic world, reliable communication channels are paramount. The Nightly Cloud Beacon provides a resilient, static web page hosted on AWS S3 and served via CloudFront. This allows the community to broadcast essential messages, 'all clear' signals, or critical updates with high availability and low maintenance.

## Features

*   **Static Website Hosting**: Leverages AWS S3 for cost-effective and durable storage of your beacon message, kept private and accessed securely via CloudFront.
*   **Global Content Delivery**: Utilizes AWS CloudFront to distribute your beacon message globally, ensuring fast access and high availability even under adverse network conditions.
*   **Customizable Message**: Easily update the beacon's message via a Terraform variable.
*   **Secure by Default**: Uses CloudFront Origin Access Control (OAC) to restrict direct public access to the S3 bucket.
*   **Simple Deployment**: Deploy with standard Terraform commands.

## Usage

To deploy your Nightly Cloud Beacon, create a `main.tf` file in your project root and reference this module:

```terraform
module "cloud_beacon" {
  source = "./path/to/nightly-cloud-beacon/src" # Adjust this path if you clone the repo

  beacon_message     = "The Nightly Integrator is online. All systems nominal."
  aws_region         = "us-east-1"
  bucket_name_prefix = "apocalypsai-beacon-prod"
}

output "beacon_url" {
  description = "The URL of the deployed CloudFront distribution for the beacon."
  value       = module.cloud_beacon.website_endpoint
}
```

Then, run the following Terraform commands:

1.  **Initialize Terraform**: `terraform init`
2.  **Review the plan**: `terraform plan`
3.  **Apply the changes**: `terraform apply`

After successful application, the `beacon_url` output will provide the URL to your deployed beacon.

## Inputs

| Name               | Description                                           | Type     | Default                       | Required |
|--------------------|-------------------------------------------------------|----------|-------------------------------|----------|
| `beacon_message`   | The message to display on the static beacon page.     | `string` | `"All Clear. Stay Vigilant."` | no       |
| `aws_region`       | The AWS region where resources will be deployed.      | `string` | `"us-east-1"`                 | no       |
| `bucket_name_prefix` | A prefix for the S3 bucket name to ensure uniqueness. | `string` | `"apocalypsai-beacon"`        | no       |

## Outputs

| Name             | Description                                       | Value Type |
|------------------|---------------------------------------------------|------------|
| `website_endpoint` | The domain name of the CloudFront distribution.   | `string`   |

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script.

```bash
cd tests/
bash test.sh
```

This script performs an offline `terraform plan` to verify that the module correctly defines the expected AWS resources without actually deploying them. It checks for the presence of an S3 bucket, a CloudFront distribution, an S3 bucket policy, and an Origin Access Control (OAC) in the generated plan.
