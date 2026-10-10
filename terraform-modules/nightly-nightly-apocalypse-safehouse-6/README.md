# Nightly Apocalypse Safehouse S3

A whimsical‑yet‑practical Terraform module that creates a **secure S3 bucket** suitable for storing critical post‑apocalyptic data.

## Features

- **Versioning** – never lose a previous version of a file.
- **Server‑side encryption** (AES‑256) – data at rest is encrypted.
- **Lifecycle rule** – automatically delete objects older than 30 days to keep the bucket tidy.
- **Read‑only IAM policy output** – easy to grant downstream services read‑only access.

## Usage

```hcl
module "safehouse" {
  source      = "./utils/nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑post‑apoc‑safehouse"
  region      = "us-east-1"
}

output "bucket_arn" {
  value = module.safehouse.bucket_arn
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique). | n/a |
| `region` | `string` | AWS region for the bucket. | `"us-east-1"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket. |
| `read_only_policy_arn` | ARN of an IAM policy granting read‑only access to the bucket. |

## Testing

A simple offline test is provided under `tests/test_module.sh`. It runs `terraform init` (backend disabled) and `terraform validate` to ensure the configuration is syntactically correct.

```bash
cd utils/nightly-apocalypse-safehouse-s3/tests
bash test_module.sh
```

## License

MIT © ApocalypsAI
