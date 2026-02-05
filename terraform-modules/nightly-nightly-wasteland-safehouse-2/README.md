# Nightly Wasteland Safehouse Terraform Module

This Terraform module creates a simple static website hosted on AWS S3 with CloudFront distribution, ideal for sharing post‑apocalyptic safehouse information. It includes a custom 404 page that displays a whimsical "The wasteland is quiet..." message.

## Usage

```hcl
module "safehouse" {
  source = "./"

  bucket_name    = "my-safehouse-site"
  domain_name    = "safehouse.example.com"
  index_document = "index.html"
  error_document = "404.html"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| domain_name | Optional custom domain for CloudFront | string | "" | no |
| index_document | Index document name | string | "index.html" | no |
| error_document | Error document name | string | "404.html" | no |

## Outputs

| Name | Description |
|------|-------------|
| website_url | URL of the S3 static website |
| cloudfront_domain | CloudFront distribution domain name |

## Testing

Run `tests/validate.sh` to ensure the module validates.
