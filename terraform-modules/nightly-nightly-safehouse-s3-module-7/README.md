# Safehouse S3 Terraform Module

A whimsical Terraform module that pretends to provision a post‑apocalyptic safe‑house S3 bucket. It creates a `null_resource` representing the bucket with versioning, encryption, and a lifecycle rule. Use it as a template for real AWS resources.

## Usage

```hcl
module "safehouse" {
  source = "git::https://github.com/polsala/ApocalypsAI.git//terraform-modules/nightly-safehouse-s3-module"

  bucket_name    = "my-safehouse-bucket"
  versioning     = true
  encryption     = "AES256"
  retention_days = 30
}
```

## Variables

- `bucket_name` – Name of the bucket (string, required)
- `versioning` – Enable versioning (bool, default true)
- `encryption` – Server‑side encryption algorithm (string, default "AES256")
- `retention_days` – Days to retain objects before deletion (number, default 30)

## Outputs

- `bucket_name` – The name of the bucket.

## Testing

Run the test script:

```sh
cd tests && ./test_module.sh
```
