# nightly-terraform-aws-s3-bucket

## Overview

A tiny, opinionated Terraform module that provisions an Amazon S3 bucket with:

* Server‑side encryption (AES‑256)
* Versioning (enabled by default)
* Strict public‑access block settings
* Optional force‑destroy and custom tags

The module is deliberately simple so it can be dropped into any Terraform configuration.

## Usage

```hcl
module "my_bucket" {
  source = "./terraform-modules/nightly-terraform-aws-s3-bucket"

  bucket_name        = "my‑awesome‑bucket"
  force_destroy      = false
  versioning_enabled = true
  tags = {
    Environment = "dev"
    Owner       = "apocalypsai"
  }
}
```

## Variables

| Name                | Type          | Default | Description |
|---------------------|---------------|---------|-------------|
| `bucket_name`       | `string`      | n/a     | Name of the S3 bucket |
| `force_destroy`     | `bool`        | `false` | Allow bucket to be destroyed even if it contains objects |
| `versioning_enabled`| `bool`        | `true`  | Enable versioning |
| `tags`              | `map(string)` | `{}`    | Tags to apply |

## Outputs

| Name          | Description |
|---------------|-------------|
| `bucket_id`   | The ID of the bucket |
| `bucket_arn`  | The ARN of the bucket |
| `bucket_region`| The region of the bucket |

## Testing

A lightweight shell test lives in `tests/validate.sh`. Run it with:

```bash
cd terraform-modules/nightly-terraform-aws-s3-bucket
bash tests/validate.sh
```

The test simply verifies that the expected resources are present in `main.tf`.
