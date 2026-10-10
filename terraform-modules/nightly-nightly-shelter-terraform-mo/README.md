# Nightly Shelter Terraform Module

## Overview

This Terraform module creates a **mock post‑apocalyptic shelter** represented by an AWS S3 bucket. The bucket name is generated from a random pet name combined with a user‑provided prefix, giving each shelter a unique, whimsical identity.

## Features

- Generates a random, human‑readable name using `random_pet`.
- Allows a custom prefix (e.g., `shelter-`) via the `bucket_name_prefix` variable.
- Outputs the final bucket name for downstream use.

## Usage

```hcl
module "shelter" {
  source            = "./utils/nightly-shelter-terraform-module"
  bucket_name_prefix = "shelter-"
}

output "shelter_bucket" {
  value = module.shelter.bucket_name
}
```

## Variables

| Name                | Type   | Description                                 | Default |
|---------------------|--------|---------------------------------------------|---------|
| `bucket_name_prefix`| string | Prefix for the generated bucket name.       | `"shelter-"` |

## Outputs

| Name        | Description                              |
|-------------|------------------------------------------|
| `bucket_name`| The full name of the created S3 bucket. |

## Testing

A simple Bash test suite lives under `tests/`. Run it with:

```bash
cd utils/nightly-shelter-terraform-module
bash tests/test_module.sh
```

The test checks that the Terraform files contain the expected resources and variables.
