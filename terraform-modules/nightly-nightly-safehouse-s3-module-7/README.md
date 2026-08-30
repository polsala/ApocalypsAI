# Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket with:

- Randomly generated name (using `random_pet`)
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule to delete non‑current versions after a configurable number of days

## Usage

```hcl
module "safehouse" {
  source = "./src"
}
```

## Inputs

| Name            | Description                                 | Type   | Default |
|-----------------|---------------------------------------------|--------|---------|
| `bucket_prefix` | Prefix for bucket name                      | string | "safehouse" |
| `lifecycle_days`| Days after which non‑current versions are deleted | number | 30 |
| `aws_region`    | AWS region                                  | string | "us-east-1" |

## Outputs

| Name       | Description                     |
|------------|---------------------------------|
| `bucket_id`| The name of the created bucket |
| `bucket_arn`| ARN of the bucket               |

## Testing

Run the test script to ensure the module validates:

```bash
bash tests/test.sh
```
