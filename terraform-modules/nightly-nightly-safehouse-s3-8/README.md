# nightly‑safehouse‑s3

A tiny Terraform module that creates a **secure S3 bucket** suitable for storing critical safe‑house data after the world ends.

## Features

- **Versioning** – keep every revision of your files.
- **Server‑side encryption** – AES‑256 encryption at rest.
- **Lifecycle rule** – automatically delete objects older than 30 days (so you don’t hoard too much junk).
- **Radiation‑level tag** – a random integer (1‑10) that pretends to measure the ambient radiation where the bucket is stored.  Great for bragging rights.

## Usage

```hcl
module "safehouse_s3" {
  source      = "./utils/terraform-modules/nightly-safehouse-s3"
  bucket_name = "my‑post‑apoc‑vault"
}
```

Run the usual Terraform workflow:

```bash
terraform init
terraform apply -var "bucket_name=my‑post‑apoc‑vault"
```

The module will output the bucket ARN and the generated radiation level.

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created bucket |
| `radiation_level` | Random integer (1‑10) representing the bucket’s radiation level |

## Testing

The module includes a deterministic unit test that validates the presence of the required resources and attributes without contacting AWS. Run it with:

```bash
python -m unittest discover -s utils/terraform-modules/nightly-safehouse-s3/tests
```

---

*Feel free to tweak the lifecycle rule or add more whimsical tags – the apocalypse is a creative playground!*
