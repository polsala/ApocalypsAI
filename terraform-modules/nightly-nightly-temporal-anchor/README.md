# Nightly Temporal Anchor Point

This Terraform module provisions a highly available static website infrastructure on AWS, consisting of an S3 bucket configured for static website hosting and a CloudFront distribution to serve its content globally.

## Whimsical Purpose

Dubbed the "Temporal Anchor Point," this utility is designed to be a resilient, low-cost beacon for broadcasting critical (or whimsically profound) information across the temporal continuum. In times of temporal flux, a stable point of reference is paramount. Deploy your most vital affirmations, paradox-proof proverbs, or simply a static page detailing the current temporal coordinates.

## Features

*   **S3 Static Website Hosting**: Cost-effective storage and serving of static content.
*   **CloudFront CDN**: Global content delivery network for low latency and high availability.
*   **Origin Access Identity (OAI)**: Restricts direct S3 bucket access, ensuring content is served only via CloudFront.
*   **HTTPS by Default**: CloudFront default certificate ensures secure delivery.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_temporal_anchor" {
  source = "./path/to/nightly-temporal-anchor/src"

  bucket_name    = "my-unique-temporal-anchor-bucket-12345"
  index_document = "affirmations.html"
  error_document = "temporal_rift.html"
  aws_region     = "us-east-1" # Or your preferred AWS region
}

output "affirmation_endpoint" {
  value       = module.my_temporal_anchor.cloudfront_domain_name
  description = "The CloudFront domain name where your temporal affirmations are broadcast."
}
```

## Inputs

| Name             | Description                                                              | Type     | Default          | Required |
|------------------|--------------------------------------------------------------------------|----------|------------------|----------|
| `bucket_name`    | The name of the S3 bucket for the static website. Must be globally unique. | `string` | n/a              | yes      |
| `domain_name`    | The custom domain name for the CloudFront distribution (optional).       | `string` | `""`             | no       |
| `index_document` | The name of the index document (e.g., `index.html`).                     | `string` | `"index.html"`   | no       |
| `error_document` | The name of the error document (e.g., `error.html`).                     | `string` | `"error.html"`   | no       |
| `aws_region`     | The AWS region to deploy resources into.                                 | `string` | `"us-east-1"`    | no       |

## Outputs

| Name                     | Description                                            |
|--------------------------|--------------------------------------------------------|
| `s3_website_endpoint`    | The S3 static website endpoint.                        |
| `cloudfront_domain_name` | The domain name of the CloudFront distribution.        |
| `cloudfront_arn`         | The ARN (Amazon Resource Name) of the CloudFront distribution. |

## Deployment

1.  **Initialize Terraform**: `terraform init`
2.  **Review Plan**: `terraform plan`
3.  **Apply Changes**: `terraform apply`

After deployment, upload your static website content (e.g., `affirmations.html`) to the created S3 bucket. The `cloudfront_domain_name` output will provide the URL to access your Temporal Anchor Point.
