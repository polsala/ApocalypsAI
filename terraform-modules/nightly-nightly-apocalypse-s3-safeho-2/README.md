# Nightly Apocalypse S3 Safehouse

## Overview
A whimsical‑yet‑useful Terraform module that creates an Amazon S3 bucket acting as a post‑apocalyptic safe‑house. The bucket comes with:

- **Versioning** enabled (so you never lose a precious artifact)
- **Server‑side encryption** (AES‑256) for data secrecy
- A **lifecycle rule** that automatically expires objects older than 30 days
- Helpful outputs for the bucket name and ARN

## Usage
```hcl
module "safehouse" {
  source      = "./src"
  bucket_name = "my-safehouse-bucket"
}
```

Run the usual Terraform workflow:
```bash
terraform init
terraform apply
```

## Testing
A lightweight Bash test validates that the module contains the required resources and settings without invoking real Terraform (offline, deterministic).
```bash
bash tests/test_main.sh
```
