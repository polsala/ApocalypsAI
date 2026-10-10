# Nightly Apocalypse Safehouse S3

## Overview

A tiny, whimsical‑yet‑practical Terraform module that creates an AWS S3 bucket designed to act as a *post‑apocalyptic safe‑house* for your critical data.

Features:
- **Versioning** – never lose a previous version of a file.
- **Server‑Side Encryption (SSE‑S3)** – data is encrypted at rest.
- **Lifecycle rule** – automatically delete objects older than 30 days to keep the bucket tidy.
- **Customizable bucket name and tags**.

## Usage

```hcl
module "safehouse" {
  source      = "./nightly-apocalypse-safehouse-s3"
  bucket_name = "my‑apocalypse‑vault"
  tags = {
    Environment = "production"
    Project     = "survival"
  }
}
```

Run the usual Terraform workflow:

```bash
terraform init
terraform apply
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `tags` | A map of tags to assign to the bucket | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created bucket |
| `bucket_arn` | The ARN of the created bucket |

## Testing

The module includes a lightweight Python test suite that validates the presence of the expected Terraform blocks without needing real AWS credentials. Run it with:

```bash
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
