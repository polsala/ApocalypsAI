# Nightly Apocalypse Safehouse S3 Terraform Module

## Overview

This Terraform module provides a **local representation** of a secure S3 bucket. It generates a JSON file containing the bucket configuration (name, versioning, encryption, and lifecycle rule). The module is completely offline‑friendly – it uses the built‑in `local` provider and does **not** require any cloud credentials.

## Features

- Bucket name is configurable via `var.bucket_name`
- Versioning is always enabled
- Server‑side encryption set to `AES256`
- Lifecycle rule to delete objects older than a configurable number of days (default: 30)
- Outputs the path to the generated JSON configuration file

## Usage

```hcl
module "safehouse_s3" {
  source          = "./nightly-apocalypse-safehouse-s3"
  bucket_name     = "my‑post‑apoc‑bucket"
  lifecycle_days  = 45
}

output "config_path" {
  value = module.safehouse_s3.config_path
}
```

Run the usual Terraform workflow:

```bash
terraform init -backend=false
terraform apply -auto-approve
```

The module will create a file like `my‑post‑apoc‑bucket.json` in the module directory containing the bucket configuration.

## Testing

A simple test script is provided under `tests/test_plan.sh`. It runs `terraform init` and `terraform plan` and verifies that the `local_file.bucket_config` resource is present in the plan.

---

*This utility lives in the `terraform-modules` classifier path, showcasing infrastructure‑as‑code capabilities.*
