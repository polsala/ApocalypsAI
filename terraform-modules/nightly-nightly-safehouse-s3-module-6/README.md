# Safehouse S3 Module

A whimsical Terraform module that creates a secure S3 bucket for storing post‑apocalyptic safe‑house data.

## Features

- Randomized bucket name using `random_pet` (if you don't provide one)
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after 30 days
- Optional tags and force‑destroy flag

## Usage

```hcl
module "safehouse" {
  source = "./"

  # Optional: provide your own bucket name
  # bucket_name = "my‑safehouse‑bucket"

  force_destroy = true
  tags = {
    Environment = "production"
    Project     = "post‑apocalypse"
  }
}
```

## Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bucket_name` | `string` | `""` | Optional explicit bucket name. If empty, a random name is generated. |
| `force_destroy` | `bool` | `false` | Whether to allow force destroy of the bucket. |
| `tags` | `map(string)` | `{}` | A map of tags to assign to the bucket. |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket. |
| `bucket_arn` | The ARN of the created S3 bucket. |

## Testing

Run the provided test script:

```bash
cd tests
./validate.sh
```

The script runs `terraform init`, `terraform validate`, and a dry‑run `terraform plan` with mock variables to ensure the module is syntactically correct.
