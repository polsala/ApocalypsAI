# Apocalyptic S3 Safehouse

Creates an AWS S3 bucket configured as a post‑apocalyptic safe‑house with versioning and a lifecycle rule that expires objects after 30 days. Ideal for storing critical logs, backups, or survival manuals.

## Usage

```bash
# Initialize Terraform
terraform init

# Provide a bucket name via tfvars
cat > terraform.tfvars <<EOF
bucket_name = "my‑apocalypse‑safehouse"
EOF

# Apply
terraform apply
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_arn`: ARN of the created bucket.
