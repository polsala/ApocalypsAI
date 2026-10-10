# Nightly Safehouse S3 Bucket

Creates an S3 bucket configured for post‑apocalyptic safe‑house data storage: versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days. Works with the AWS provider.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

Run the usual Terraform workflow:

```bash
terraform init
terraform apply
```

## Variables

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket to create | `string` | yes |

## Resources Created

- `aws_s3_bucket.safehouse` – the bucket with versioning, AES‑256 encryption, and a lifecycle rule that deletes objects older than 30 days.

## Testing

A simple deterministic test script is provided under `tests/` that runs `terraform validate` and checks that the expected resources and blocks are present in the plan.
