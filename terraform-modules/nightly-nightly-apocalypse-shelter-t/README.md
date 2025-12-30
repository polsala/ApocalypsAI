# Terraform Apocalyptic Shelter Module

A whimsical yet practical Terraform module that creates a resilient "shelter" for hosting static
content in the cloud. It provisions:

* An S3 bucket with versioning and server‑side encryption.
* A CloudFront distribution that serves the bucket with a custom error page (perfect for
  post‑apocalyptic themed sites).
* An IAM role with the minimal permissions required for CloudFront to read from the bucket.

## Usage

```hcl
module "shelter" {
  source          = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-shelter-terraform"
  bucket_name     = "my‑post‑apoc‑shelter"
  index_document  = "index.html"
  error_document  = "error.html"
  region          = "us-east-1"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket (must be globally unique) | string | n/a | yes |
| index_document | Index document for the bucket website | string | "index.html" | no |
| error_document | Custom error document for the bucket website | string | "error.html" | no |
| region | AWS region for resources | string | "us-east-1" | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_arn | ARN of the created S3 bucket |
| cloudfront_domain_name | Domain name of the CloudFront distribution |

## Testing

Run the provided test script:

```sh
cd tests && ./validate.sh
```

The script runs `terraform init -backend=false` and `terraform validate` to ensure the
module syntax is correct without contacting AWS.

## License

MIT
