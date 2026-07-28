# Safehouse S3 Terraform Module

Creates an AWS S3 bucket designed as a post‑apocalyptic safe‑house. The bucket has versioning, server‑side encryption, and a lifecycle rule that automatically deletes objects older than 30 days. If you don't provide a bucket name, a whimsical random name is generated.

## Usage

```hcl
module "safehouse" {
  source      = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-safehouse-s3"
  aws_region  = "us-west-2"
  bucket_name = "my‑safe‑house"
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| aws_region | AWS region for the bucket | string | "us-east-1" |
| bucket_name | Optional bucket name; if empty a random name is generated | string | "" |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created S3 bucket |
| bucket_arn | The ARN of the created S3 bucket |

## Testing

Run the test script:

```sh
cd tests && ./test_main.sh
```
