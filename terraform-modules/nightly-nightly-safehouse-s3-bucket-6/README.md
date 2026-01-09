# nightly‑safehouse‑s3‑bucket

A tiny Terraform module that pretends to create a post‑apocalyptic safe‑house S3 bucket.  It demonstrates how to configure:

* Bucket name
* Versioning (enabled/disabled)
* Server‑side encryption (enabled/disabled)
* Lifecycle rule to delete objects after a configurable number of days

The module is **offline‑friendly** – it uses the `null` provider so you can run `terraform validate` without any cloud credentials.

## Usage
```hcl
module "safehouse" {
  source = "./nightly-safehouse-s3-bucket"

  bucket_name        = "my‑safehouse"
  versioning_enabled = true
  encryption_enabled = true
  lifecycle_days     = 30
}
```

## Variables
| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the imagined bucket | `"safehouse-bucket"` |
| `versioning_enabled` | `bool` | Whether versioning is on | `true` |
| `encryption_enabled` | `bool` | Whether server‑side encryption is on | `true` |
| `lifecycle_days` | `number` | Days after which objects are deleted | `30` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_name` | The bucket name you supplied |
| `versioning_enabled` | Echoes the versioning flag |
| `encryption_enabled` | Echoes the encryption flag |
| `lifecycle_days` | Echoes the lifecycle period |

## Testing
Run the provided test script:
```bash
cd nightly-safehouse-s3-bucket/tests
./test.sh
```
It will initialise the module (backend disabled) and run `terraform validate`.  All tests should pass offline.
