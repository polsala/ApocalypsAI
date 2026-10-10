# Nightly Safehouse S3

This Terraform module creates an S3 bucket that serves as a post‑apocalyptic safe‑house for your data. The bucket name is generated from a random pet name, making each deployment unique and whimsical.

## Features

- **Random, memorable bucket name** using `random_pet`.
- **Versioning** enabled to keep historic copies.
- **Server‑side encryption** with AES‑256.
- **Lifecycle rule** that deletes objects older than 30 days.
- Fully **self‑contained** – no external state backend required for testing.

## Usage

```hcl
module "safehouse" {
  source = "./utils/nightly-safehouse-s3"
  region = "us-east-1"
}
```

Run the usual Terraform workflow:

```bash
terraform init -backend=false   # offline, no remote backend
terraform apply -auto-approve
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `region` | AWS region for the bucket | string | `"us-east-1"` |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | The generated bucket name |
| `bucket_arn`  | ARN of the bucket |

## Testing

The module includes a lightweight Python test that validates the generated Terraform configuration contains the expected resources. Run it with:

```bash
python -m unittest discover -s utils/nightly-safehouse-s3/tests
```

---

*Happy storing!*
