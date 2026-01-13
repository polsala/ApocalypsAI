# Nightly Safehouse S3 Bucket

A tiny Terraform module that creates an AWS S3 bucket suitable for storing critical postâapocalyptic data. The bucket has versioning enabled and a lifecycle rule that expires objects older than 365 days.

## Features

- **Versioning** â never lose a previous version of a file.
- **Lifecycle rule** â automatically delete objects older than one year to keep storage costs low.
- **Zeroâruntime dependencies** â pure Terraform, works with any backend.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "myâpostâapocâsafehouse"
}

output "bucket_arn" {
  value = module.safehouse.bucket_arn
}
```

## Variables

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket to create. Must be globally unique. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket. |

## Testing

Run the provided test script (requires Terraform 1.0+):

```bash
chmod +x tests/test.sh
./tests/test.sh
```

The script validates the configuration and checks that the required blocks are present.

