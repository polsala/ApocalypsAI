# nightly‑safehouse‑s3‑module

A playful Terraform module that pretends to create an S3 bucket for your post‑apocalyptic safe‑house. It uses the **null** provider so it never touches real cloud resources, making it safe to run in CI.

## Features

- Configurable bucket name (default: `apocalypse-safehouse`)
- Optional versioning flag (default: `true`)
- Outputs the bucket name for downstream modules
- Fully testable offline with `terraform validate` and a tiny Bash test script

## Usage

```hcl
module "safehouse" {
  source      = "./nightly-safehouse-s3-module"
  bucket_name = "my‑post‑apoc‑vault"
  versioning  = true
}

output "bucket" {
  value = module.safehouse.bucket_name
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the mock S3 bucket | `string` | `"apocalypse-safehouse"` |
| `versioning`  | Whether versioning is enabled (informational only) | `bool` | `true` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | The bucket name passed to the module |

## Testing

The module includes an offline test script located at `tests/test_module.sh`. Run it with:

```bash
cd nightly-safehouse-s3-module
bash tests/test_module.sh
```

The script runs `terraform init`, `terraform validate`, and checks that the expected `null_resource` appears in the plan.
