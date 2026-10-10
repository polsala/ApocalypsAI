# Nightly Safehouse S3

Utility creates an S3 bucket for post‑apocalyptic safehouse storage with versioning, server‑side encryption, a lifecycle rule, and a random pet name for the bucket.

## Usage

```sh
cd utils/nightly-safehouse-s3
terraform init -backend=false
terraform apply -auto-approve
```

The module will output the bucket name.

## Variables

- `region` – AWS region (default: `us-east-1`).
- `environment` – Deployment environment tag (default: `dev`).

## Outputs

- `bucket_name` – Name of the created S3 bucket.

## Testing

Run the validation script to ensure the Terraform configuration is syntactically correct:

```sh
./tests/validate.sh
```
