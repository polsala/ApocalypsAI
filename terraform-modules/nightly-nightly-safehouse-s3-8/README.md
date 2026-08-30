# Nightly Safehouse S3

A whimsical Terraform module that provisions a secure S3 bucket for post‑apocalyptic data hoarding. The bucket has versioning, server‑side encryption, and a lifecycle rule that expires objects after 30 days.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my‑post‑apoc‑vault"
}
```

Run `terraform init && terraform apply` to create the bucket (requires AWS credentials).

## Features

- Versioning enabled
- AES‑256 encryption
- Lifecycle rule: delete objects older than 30 days
- Outputs the bucket ARN

## Testing

```sh
cd tests
./test_module.sh
```
