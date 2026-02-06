# Nightly Safehouse S3 Bucket

This Terraform module creates an Amazon S3 bucket designed as a post‑apocalyptic safe‑house.

## Features

- **Randomized safe‑house name**: combines a user‑provided prefix with a random pet name.
- **Versioning enabled** so you never lose a precious stash.
- **Lifecycle rule** that expires non‑current object versions after 30 days.
- **No remote backend required** – works with local state for quick testing.

## Usage

```hcl
module "safehouse" {
  source             = "./src"
  bucket_name_prefix = "my-safehouse"
  tags = {
    Environment = "production"
    Project     = "ApocalypsAI"
  }
}
```

Run the following commands to test locally:

```bash
cd src
terraform init -backend=false
terraform validate
```

## Inputs

| Name               | Description                                 | Type   | Default | Required |
|--------------------|---------------------------------------------|--------|---------|----------|
| `bucket_name_prefix` | Prefix for the bucket name (will be suffixed with a random pet). | `string` | n/a     | yes      |
| `tags`               | Map of tags to apply to the bucket.          | `map(string)` | `{}`   | no       |

## Outputs

| Name       | Description                     |
|------------|---------------------------------|
| `bucket_id` | The name of the created bucket |
| `bucket_arn`| The ARN of the created bucket   |

## Testing

A simple validation script is provided under `tests/validate.sh` which runs `terraform init` and `terraform validate`.
