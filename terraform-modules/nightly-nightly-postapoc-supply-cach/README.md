# Post‑Apocalyptic Supply Cache Terraform Module

Creates an AWS S3 bucket with versioning and lifecycle rules, plus a randomly named object containing a whimsical "supply cache" note. Ideal for storing emergency data in a resilient bucket.

## Usage

```hcl
module "supply_cache" {
  source      = "github.com/yourorg/ApocalypsAI//terraform-modules/nightly-postapoc-supply-cache"
  bucket_name = "my-safehouse-bucket"
  region      = "us-east-1"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `region` (string, optional, default "us-east-1"): AWS region.

## Outputs

- `bucket_id`
- `bucket_arn`
- `supply_object_key`

## Notes

The module uses the `random_pet` provider to generate a whimsical object key like `supply-cache-<adjective>-<noun>.txt`.
