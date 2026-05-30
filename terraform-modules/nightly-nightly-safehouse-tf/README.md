# Nightly Safehouse Terraform Module

A tiny Terraform module that provisions a secure S3 bucket with versioning, server‑side encryption, and a restrictive bucket policy. Perfect for storing apocalypse‑style survival data, backups, or any critical files.

## Usage

```hcl
module "safehouse" {
  source      = "git::https://github.com/your-org/ApocalypsAI.git//terraform-modules/nightly-safehouse-tf"
  bucket_name = "my-apocalypse-data"
  region      = "us-east-1"
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket (must be globally unique) | string | n/a | yes |
| region | AWS region for the bucket | string | "us-east-1" | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Testing

Run the provided test script:

```sh
cd tests && ./test_main.sh
```

It will initialise the module and run `terraform validate`.
