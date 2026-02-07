# Nightly Safehouse S3 Module

## Overview

A whimsical yet practical Terraform module that creates an Amazon S3 bucket configured for maximum durability and security – perfect for storing critical data in a post‑apocalyptic safe‑house scenario.

## Features

- **Versioning** – keep every version of an object.
- **SSE‑S3 Encryption** – server‑side encryption at rest.
- **Lifecycle Rule** – automatically delete objects older than 30 days.
- **Public Access Block** – prevents accidental public exposure.
- **Custom Tags** – add any tags you need.

## Usage Example

```hcl
module "safehouse_bucket" {
  source      = "./utils/nightly-safehouse-s3-module"
  bucket_name = "my‑safehouse‑data"
  tags = {
    Environment = "post‑apocalypse"
    Owner       = "survivors"
  }
}
```

## Variables

| Name | Type | Description | Required |
|------|------|-------------|----------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique). | yes |
| `tags` | `map(string)` | Optional tags to apply to the bucket. | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |

## Requirements

- Terraform >= 1.0.0
- AWS provider configured with appropriate credentials.

## Testing

Run the automated tests with:

```bash
python -m unittest discover -s tests
```

The tests verify that the module contains the expected resources and configuration blocks.
