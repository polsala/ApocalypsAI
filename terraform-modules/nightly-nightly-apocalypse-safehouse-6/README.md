# Apocalyptic Safehouse S3 Terraform Module

A whimsical yet practical Terraform module that creates a version‑controlled S3 bucket, applies a lifecycle rule to delete old objects, and attaches a minimal IAM policy allowing read‑only access. Perfect for storing survival manuals, ration logs, or any post‑apocalypse data.

## Usage

```hcl
module "safehouse_s3" {
  source      = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "post-apocalypse"
    Owner       = "survivors"
  }
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| bucket_name | Name of the S3 bucket | string | yes |
| tags | Map of tags to apply | map(string) | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Testing

Run the provided test script:

```sh
cd terraform-modules/nightly-apocalypse-safehouse-s3
./tests/validate.sh
```
