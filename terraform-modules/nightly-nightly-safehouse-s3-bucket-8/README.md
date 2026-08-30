# nightly-safehouse-s3-bucket

A tiny Terraform module that creates a **secure S3 bucket** suitable for storing precious post‑apocalyptic data.

## Features

- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule that expires objects older than 30 days
- Minimal provider configuration that works offline (uses mock credentials)

## Usage

```hcl
module "safehouse" {
  source      = "./utils/terraform-modules/nightly-safehouse-s3-bucket"
  bucket_name = "my‑post‑apoc‑vault"
}

output "bucket_arn" {
  value = module.safehouse.bucket_arn
}
```

## Variables

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket to create | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |

## Testing

Run the provided test script:

```bash
cd utils/terraform-modules/nightly-safehouse-s3-bucket
bash tests/test_module.sh
```

The script runs `terraform init`, `terraform validate`, and a mock `terraform plan` to ensure the module is syntactically correct.
