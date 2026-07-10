# Safehouse S3 Terraform Module

Creates an AWS S3 bucket designed as a post‑apocalyptic safehouse. The bucket has versioning enabled, server‑side encryption, and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days. Tags can be supplied to identify the safehouse.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my‑safehouse‑bucket"
  tags = {
    Environment = "post‑apocalypse"
    Owner       = "survivors"
  }
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| bucket_name | Name of the S3 bucket | string | yes |
| tags | Tags to apply to the bucket | map(string) | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the bucket |
| bucket_arn | The ARN of the bucket |
