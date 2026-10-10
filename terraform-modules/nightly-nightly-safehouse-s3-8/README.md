# nightly‑safehouse‑s3

A whimsical yet practical Terraform module that creates an **S3 Safehouse** – a version‑enabled bucket with lifecycle rules to archive old data to Glacier and a pre‑seeded "starter supply" object.

## Features

- Configurable bucket name prefix
- Versioning enabled (so you never lose a crucial file)
- Lifecycle rule: move objects to Glacier after 30 days, delete after 365 days
- Optional starter supply object (e.g., "Emergency rations.txt")
- Outputs for bucket ID, ARN, and starter‑supply URL

## Usage

```hcl
module "safehouse" {
  source               = "./utils/terraform-modules/nightly-safehouse-s3"
  bucket_name_prefix   = "my‑post‑apoc"
  region               = "us-west-2"
  supply_content       = "Emergency rations: water, beans, and hope."
}

output "safehouse_bucket" {
  value = module.safehouse.bucket_id
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name_prefix` | Prefix for the bucket name (final name will be `${prefix}-${random_id}`) | `string` | `"safehouse"` |
| `region` | AWS region for the bucket | `string` | `"us-east-1"` |
| `supply_content` | Content of the starter‑supply object | `string` | `"Emergency rations"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |
| `supply_url` | HTTPS URL of the starter‑supply object |

## Testing

Run the bundled test script:

```bash
cd utils/terraform-modules/nightly-safehouse-s3/tests
bash test_module.sh
```

The script validates the configuration and checks that the expected resources are defined.
