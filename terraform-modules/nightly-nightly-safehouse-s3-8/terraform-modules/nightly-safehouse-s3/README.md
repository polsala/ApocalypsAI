# Nightly Safehouse S3

Terraform module to create an S3 bucket configured for post‑apocalyptic safe‑house storage. The bucket has versioning enabled, server‑side encryption, and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days.

## Usage

```hcl
module "safehouse_s3" {
  source = "./terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
  tags        = {
    Environment = "post-apocalypse"
    Owner       = "survivors"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| tags | Tags to apply to the bucket | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | ARN of the bucket |

## Testing

Run `tests/test.sh` from the module root. It will initialize Terraform, validate the configuration, and ensure the plan contains the expected resources.
