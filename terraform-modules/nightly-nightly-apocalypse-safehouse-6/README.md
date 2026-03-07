# Apocalyptic Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket that acts as a post‑apocalyptic safe‑house for your data. The bucket is:

- Uniquely named using `random_pet` (e.g., `radiated-fox`).
- Versioned and encrypted with AES‑256.
- Configured with a lifecycle rule that deletes non‑current versions after 30 days.

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse-s3"

  # optional: custom bucket name
  bucket_name = "my-custom-safehouse"
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| bucket_name | Custom bucket name; if omitted a random pet name is generated. | string | null |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket. |
| bucket_arn | The ARN of the created bucket. |

## Testing

Run the provided test script:

```sh
cd tests && ./test_module.sh
```
