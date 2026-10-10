# Nightly Cloud Sanctuary Beacon

A Terraform module designed to provision a highly available, resilient static website on AWS, acting as a digital sanctuary beacon for community messages, emergency broadcasts, or shared wisdom in the post-apocalyptic landscape.

## Features

*   **Static Website Hosting**: Leverages AWS S3 for cost-effective and scalable static content storage.
*   **Global Content Delivery**: Utilizes AWS CloudFront for low-latency content delivery and HTTPS.
*   **Custom Domain Support**: Optionally integrates with AWS Route 53 for custom domain names.
*   **Secure Access**: Configures S3 bucket policies and CloudFront Origin Access Control (OAC) for secure content delivery.
*   **Whimsical Resilience**: A digital whisper in the void, always there, always accessible.

## Usage

This module creates the necessary AWS resources for a static website. You'll need to upload your `index.html`, `error.html`, and other static assets to the created S3 bucket.

### Prerequisites

*   An AWS account with appropriate permissions to create S3 buckets, CloudFront distributions, and Route 53 records.
*   Terraform CLI installed.
*   AWS CLI configured with credentials.

### Example

```terraform
module "sanctuary_beacon" {
  source = "./src" # Or a Git URL if published

  bucket_name_prefix = "apocalypsai-beacon"
  domain_name        = "beacon.example.com" # Optional: if you own this domain in Route 53
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
  }
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = module.sanctuary_beacon.cloudfront_domain_name
}

output "s3_bucket_website_endpoint" {
  description = "The S3 bucket website endpoint."
  value       = module.sanctuary_beacon.s3_bucket_website_endpoint
}
```

### Inputs

| Name                 | Description                                                               | Type     | Default | Required |
| :------------------- | :------------------------------------------------------------------------ | :------- | :------ | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. The full name will be generated.         | `string` | `null`  | yes      |
| `domain_name`        | (Optional) The custom domain name for the CloudFront distribution.        | `string` | `null`  | no       |
| `tags`               | A map of tags to assign to the resources.                                 | `map`    | `{}`    | no       |

### Outputs

| Name                       | Description                                   |
| :------------------------- | :-------------------------------------------- |
| `s3_bucket_id`             | The ID of the S3 bucket.                      |
| `s3_bucket_arn`            | The ARN of the S3 bucket.                     |
| `s3_bucket_website_endpoint` | The S3 bucket website endpoint.             |
| `cloudfront_distribution_id` | The ID of the CloudFront distribution.      |
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution. |

## Development & Testing

To test this module locally:

1.  Navigate to the `tests/` directory.
2.  Run the `test.sh` script: `./test.sh`

This script will run `terraform init -backend=false`, `terraform validate`, and `terraform plan -detailed-exitcode` to ensure the module is syntactically correct and produces a valid plan without actually provisioning resources.
