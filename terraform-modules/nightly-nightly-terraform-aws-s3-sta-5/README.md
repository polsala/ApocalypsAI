# Terraform AWS S3 Static Website Module

This module creates an S3 bucket configured for static website hosting. Optionally it can also create a CloudFront distribution to serve the site over CDN.

## Usage

```hcl
module "static_website" {
  source = "./"

  bucket_name        = "my-website-bucket"
  index_document     = "index.html"
  error_document     = "error.html"
  enable_cloudfront  = true
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| index_document | Index document for website | string | "index.html" | no |
| error_document | Error document for website | string | "error.html" | no |
| enable_cloudfront | Whether to create CloudFront distribution | bool | false | no |
| aws_region | AWS region for resources | string | "us-east-1" | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_arn | ARN of the S3 bucket |
| website_endpoint | Website endpoint URL |
| cloudfront_distribution_id | ID of CloudFront distribution (if created) |

## Testing

Run the test script:

```sh
cd tests && ./run.sh
```
