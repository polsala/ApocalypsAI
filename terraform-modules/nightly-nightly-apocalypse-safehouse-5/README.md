# nightly‑apocalypse‑safehouse‑s3

A whimsical Terraform module that pretends to create an S3 bucket for a post‑apocalyptic safe‑house.  It uses only the `local` and `null` providers so it can be validated and tested completely offline.

## Features

- Configurable bucket name
- Optional versioning flag (default: enabled)
- Configurable lifecycle rule that “deletes” objects after a number of days (simulated via a `null_resource`)
- Writes the bucket name to a local file so you can see the result without any cloud access

## Usage

```hcl
module "safehouse_bucket" {
  source            = "./utils/terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name       = "my‑post‑apoc‑safehouse"
  versioning_enabled = true
  lifecycle_days    = 45
}
```

## Inputs

| Name                | Description                                 | Type   | Default |
|---------------------|---------------------------------------------|--------|---------|
| `bucket_name`       | Name of the (mock) S3 bucket                | string | n/a (required) |
| `versioning_enabled`| Whether versioning is enabled (simulated)  | bool   | `true` |
| `lifecycle_days`    | Days after which objects are “deleted” (simulated) | number | `30` |

## Outputs

| Name          | Description                     |
|---------------|---------------------------------|
| `bucket_name` | The bucket name passed in input |

## Testing

The module includes an offline test script that runs `terraform init`, `validate` and a dry‑run `plan`.  No cloud credentials are required.

```bash
cd utils/terraform-modules/nightly-apocalypse-safehouse-s3/tests
./test_module.sh
```

If the script exits with code 0, the module passed all checks.
