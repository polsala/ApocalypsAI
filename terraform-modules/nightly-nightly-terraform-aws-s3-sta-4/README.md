# nightly-terraform-aws-s3-static-site

## Overview
A tiny, self‑contained Terraform module that provisions an Amazon S3 bucket configured for static website hosting.  Optionally it can also create a CloudFront distribution to serve the site over a CDN with HTTPS.

## Features
- Creates an S3 bucket with `website` configuration.
- Optional CloudFront distribution with default cache behavior.
- Fully configurable via input variables.
- Outputs useful identifiers for downstream modules.

## Usage
```hcl
module "static_site" {
  source          = "./utils/nightly-terraform-aws-s3-static-site"
  bucket_name     = "my‑awesome‑site"
  enable_cdn      = true
  index_document  = "index.html"
  error_document  = "error.html"
}
```

## Variables
| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique). | n/a |
| `enable_cdn` | `bool` | Whether to create a CloudFront distribution. | `false` |
| `index_document` | `string` | S3 website index document. | `"index.html"` |
| `error_document` | `string` | S3 website error document. | `"error.html"` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket. |
| `bucket_arn` | The ARN of the created S3 bucket. |
| `cloudfront_domain` | The domain name of the CloudFront distribution (only if `enable_cdn` is true). |

## Testing
Run the provided test script to verify that the module files contain the expected resources and variables:
```bash
cd utils/nightly-terraform-aws-s3-static-site/tests
bash test_module.sh
```
The script runs offline and uses simple `grep` checks.  It is safe to execute in any environment.

## License
MIT © ApocalypsAI
