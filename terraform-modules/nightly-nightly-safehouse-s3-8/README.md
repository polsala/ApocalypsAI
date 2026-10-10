# Nightly Safehouse S3 Terraform Module

This module provisions an S3 bucket configured for post‑apocalyptic data hoarding. Features:

- Versioning enabled
- Server‑side encryption (AES‑256)
- Lifecycle rule that deletes objects older than 30 days
- Simple tag for identification

## Usage

```hcl
module "safehouse" {
  source      = "./src"
  bucket_name = "my-safe-house"
}
```

Run the usual Terraform workflow:

```bash
terraform init
terraform apply
```

## Testing

A deterministic test script is provided. Execute it with:

```bash
bash tests/test_module.sh
```

The script runs `terraform validate` and ensures the plan contains the expected `aws_s3_bucket.safehouse` resource.
