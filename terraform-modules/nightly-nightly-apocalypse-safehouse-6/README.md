# Apocalyptic Safehouse S3 Module

Creates an S3 bucket configured for post‑apocalyptic data hoarding.

## Features

- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule to delete non‑current versions after 30 days
- IAM policy for read‑only access to the bucket

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safe-house"
}
```

Run the usual Terraform commands:

```bash
terraform init
terraform apply
```

## Variables

| Name | Description | Type |
|------|-------------|------|
| `bucket_name` | Name of the S3 bucket | `string` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |
| `read_only_policy_arn` | ARN of the read‑only IAM policy |

## Testing

A deterministic offline test is provided in `tests/test_module.sh`. It uses a mock AWS provider configuration and validates the module without contacting real AWS services.
