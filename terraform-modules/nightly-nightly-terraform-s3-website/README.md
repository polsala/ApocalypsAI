# nightly-terraform-s3-website

Terraform module to provision an AWS S3 bucket configured for static website hosting, with optional CloudFront distribution and bucket policy for public read.

## Usage

```hcl
module "static_site" {
  source = "./src"

  bucket_name    = "my-website-bucket"
  index_document = "index.html"
  error_document = "error.html"
  enable_cdn     = true
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `index_document` (string, default `"index.html"`): Index document for the website.
- `error_document` (string, default `"error.html"`): Error document for the website.
- `enable_cdn` (bool, default `false`): Whether to create a CloudFront distribution.

## Outputs

- `bucket_id`: ID of the created S3 bucket.
- `website_endpoint`: Website endpoint URL of the S3 bucket.
- `cloudfront_domain`: Domain name of the CloudFront distribution (only when `enable_cdn` is true).

## Testing

Run the test script to verify that required Terraform resources are defined:

```bash
bash tests/test_main.sh
```
