# Nightly Apocalypse Safehouse S3

Utility Terraform module that provisions a secure S3 bucket for storing post‑apocalyptic supplies.

## Features

- **Versioning** enabled so you never lose a previous supply list.
- **Server‑side encryption** (AES‑256) for all objects.
- **Lifecycle rule** that automatically deletes objects older than 30 days – perfect for rotating rations.
- Optional **initial `supply-cache.txt` object** with placeholder content.

## Usage Example

```hcl
module "safehouse" {
  source               = "./nightly-apocalypse-safehouse-s3"
  bucket_name          = "my‑post‑apoc‑supplies"
  create_initial_object = true
  initial_content      = "Water, canned beans, solar charger"
}

output "bucket_id" {
  value = module.safehouse.bucket_id
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket to create. | n/a |
| `create_initial_object` | `bool` | Whether to create the starter `supply-cache.txt` object. | `true` |
| `initial_content` | `string` | Content of the starter object. | `"Emergency supplies placeholder"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |
| `initial_object_key` | Key of the starter object (empty string if not created). |

## Testing

The module includes a simple validation test that runs `terraform init` (without a backend) and `terraform validate`.

```bash
cd nightly-apocalypse-safehouse-s3/tests
./validate.sh
```

If the script exits with code 0, the module syntax is valid.
