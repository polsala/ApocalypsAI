# Terraform AWS S3 Static Site

## Overview
This module creates an S3 bucket configured for static website hosting. Optionally it can also create a CloudFront distribution for CDN.

## Usage
```hcl
module "static_site" {
  source = "github.com/yourorg/polsala/terraform-modules/nightly-terraform-aws-s3-static-site"
  bucket_name = "my-website-bucket"
  enable_cdn  = true
}
```

## Inputs
- `bucket_name` (string, required): Name of the S3 bucket.
- `enable_cdn` (bool, default false): Whether to create a CloudFront distribution.

## Outputs
- `bucket_arn`
- `cloudfront_domain_name` (if CDN enabled)

## Requirements
- Terraform >= 1.0
- AWS provider
