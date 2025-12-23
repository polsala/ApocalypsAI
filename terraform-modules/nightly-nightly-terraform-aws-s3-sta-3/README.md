# Nightly Terraform AWS S3 Static Website Module

## Overview

This Terraform module creates an Amazon S3 bucket configured for static website hosting.  Optionally, it can also provision a CloudFront distribution in front of the bucket for CDN capabilities, custom domain support, and HTTPS.

## Features

- S3 bucket with public read access and website configuration.
- Optional CloudFront distribution with default security settings.
- Configurable bucket name, index/error documents, and CloudFront price class.
- Outputs useful values such as the bucket ARN, website endpoint, and CloudFront domain name.

## Usage

```hcl
module "static_website" {
  source = "./utils/nightly-terraform-aws-s3-static-website"

  bucket_name        = "my-awesome-site"
  index_document     = "index.html"
  error_document     = "error.html"
  enable_cloudfront  = true
  cf_price_class     = "PriceClass_100"
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `index_document` | Index document for the website (e.g., `index.html`) | `string` | `"index.html"` | no |
| `error_document` | Error document for the website (e.g., `error.html`) | `string` | `"error.html"` | no |
| `enable_cloudfront` | Whether to create a CloudFront distribution in front of the bucket | `bool` | `false` | no |
| `cf_price_class` | CloudFront price class (`PriceClass_100`, `PriceClass_200`, `PriceClass_All`) | `string` | `"PriceClass_100"` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket |
| `website_endpoint` | S3 website endpoint URL |
| `cloudfront_domain` | Domain name of the CloudFront distribution (empty if disabled) |

## Testing

Run the provided test script to ensure the module validates correctly:

```bash
cd utils/nightly-terraform-aws-s3-static-website/tests
./validate.sh
```

The script runs `terraform init -backend=false` and `terraform validate` on an example configuration.

## License

MIT © ApocalypsAI Community
