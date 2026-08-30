# Nightly Safehouse S3 Module

A tiny Terraform module that creates an AWS S3 bucket with versioning enabled and a lifecycle rule that expires objects after 365 days. Perfect for storing precious supplies in the wasteland.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my‑post‑apoc‑store"
}
```

Run `terraform init && terraform apply`.

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| bucket_name | Name of the S3 bucket | string | yes |

## Outputs

| Name | Description |
|------|-------------|
| bucket_arn | ARN of the created bucket |
