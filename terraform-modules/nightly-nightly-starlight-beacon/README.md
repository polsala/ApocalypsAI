# Nightly Starlight Beacon

Provisions a highly available, secure static website on AWS S3 and CloudFront to broadcast vital community messages across the digital wasteland.

## Overview

This Terraform module creates the necessary AWS infrastructure for a static website:

*   An S3 bucket to store your website's content (HTML, CSS, JS, images).
*   An AWS CloudFront distribution to serve your content globally with low latency, caching, and HTTPS.
*   An Origin Access Control (OAC) to securely restrict direct access to the S3 bucket, ensuring content is only served via CloudFront.

This setup is ideal for broadcasting important announcements, emergency protocols, or simply sharing whimsical tales with the community.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

### Prerequisites

*   Terraform CLI installed.
*   AWS CLI configured with appropriate credentials and default region.

### Example `main.tf`

```terraform
module "starlight_beacon" {
  source = "./path/to/nightly-starlight-beacon/src" # Adjust this path to where you place the module

  bucket_name = "my-apocalypsai-beacon-website"
  index_document = "index.html"
  error_document = "error.html"
  aliases = ["beacon.example.com"]
  acm_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" # Optional: Replace with your ACM certificate ARN

  tags = {
    Project = "ApocalypsAI"
    Environment = "Production"
  }
}

output "website_url" {
  description = "The URL of the deployed static website."
  value       = "https://${module.starlight_beacon.cloudfront_domain_name}"
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket where content should be uploaded."
  value       = module.starlight_beacon.s3_bucket_id
}
```

### Uploading Content

After `terraform apply`, upload your static website files to the S3 bucket specified by the `s3_bucket_name` output. For example:

```bash
aws s3 sync ./my-website-content/ s3://$(terraform output -raw s3_bucket_name) --delete
```

## Module Inputs

| Name                  | Description                                                              | Type          | Default       | Required |
|-----------------------|--------------------------------------------------------------------------|---------------|---------------|----------|
| `bucket_name`         | The name of the S3 bucket to create for the static website.              | `string`      | n/a           | yes      |
| `index_document`      | The default document for the website (e.g., `index.html`).               | `string`      | `"index.html"`| no       |
| `error_document`      | The error document for the website (e.g., `error.html`).                 | `string`      | `"error.html"`| no       |
| `aliases`             | A list of CNAMEs (domain names) for the CloudFront distribution.         | `list(string)`| `[]`          | no       |
| `acm_certificate_arn` | The ARN of an AWS Certificate Manager (ACM) certificate for custom domains. Required if `aliases` are provided. | `string`      | `null`        | no       |
| `tags`                | A map of tags to assign to the resources.                                | `map(string)` | `{}`          | no       |

## Module Outputs

| Name                         | Description                                  |
|------------------------------|----------------------------------------------|
| `s3_bucket_id`               | The ID of the S3 bucket.                     |
| `s3_bucket_regional_domain_name` | The regional domain name of the S3 bucket.   |
| `cloudfront_domain_name`     | The domain name of the CloudFront distribution. |
| `cloudfront_hosted_zone_id`  | The CloudFront Hosted Zone ID.               |

## Tests

To run the module's tests, navigate to the module directory and execute:

```bash
terraform test
```

These tests use `mock_provider` to ensure determinism and run offline without requiring AWS credentials.
