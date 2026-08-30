# Terraform S3 Static Site Module

## Overview
A tiny Terraform module that creates an AWS S3 bucket configured for static website hosting. It also attaches a bucket policy that makes the bucket publicly readable.

## Variables
- `bucket_name` (string, required): Name of the S3 bucket.
- `index_document` (string, default: "index.html"): The index document for the website.
- `error_document` (string, default: "error.html"): The error document for the website.

## Outputs
- `bucket_id` – The ID of the created bucket.
- `website_endpoint` – The website endpoint URL.

## Usage
```hcl
module "static_site" {
  source          = "github.com/your-org/terraform-modules//nightly-terraform-s3-site"
  bucket_name     = "my-unique-bucket"
  index_document  = "index.html"
  error_document  = "error.html"
}
```

## Notes
- The module does **not** configure DNS or CloudFront. It only creates the bucket and makes it publicly readable.
- Ensure the bucket name is globally unique.
