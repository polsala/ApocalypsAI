# Nightly Safehouse S3 Bunker

Creates an S3 bucket with:

* Randomly generated name (using `random_pet`)
* Versioning enabled
* Server‑side AES‑256 encryption
* Lifecycle rule that expires objects after 30 days
* Optional prefix for the bucket name

## Usage

```hcl
module "safehouse" {
  source        = "git::https://github.com/yourorg/polsala.git//terraform-modules/nightly-safehouse-s3-bunker"
  bucket_prefix = "prep"  # optional, defaults to "safehouse"
}
```

The module will output the final bucket name:

```hcl
output "bucket_name" {
  value = module.safehouse.bucket_name
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_prefix` | Prefix for the bucket name (combined with a random pet name) | `string` | `"safehouse"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | The name of the created S3 bucket |

## Notes

* The bucket is created with `force_destroy = true` so it can be removed even if it contains objects – handy for testing.
* No AWS credentials are required to run the tests; they only verify the Terraform code structure.
