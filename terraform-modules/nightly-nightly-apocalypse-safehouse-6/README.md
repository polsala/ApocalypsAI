# Apocalyptic Safehouse S3 Module

Creates an S3 bucket configured for post‑apocalyptic data hoarding. Features versioning, server‑side encryption, a lifecycle rule to transition old versions to Glacier, and an IAM policy granting read/write to a specified IAM role.

## Usage

```hcl
module "safehouse" {
  source            = "github.com/yourorg/apocalypse-modules//nightly-apocalypse-safehouse-s3"
  bucket_name       = "my-safehouse-bucket"
  allowed_role_name = "SurvivorRole"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `allowed_role_name` (string, required): Name of the IAM role allowed to access the bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.
- `policy_arn` – ARN of the IAM policy attached.

## Testing

Run the validation script:

```bash
cd tests && ./validate.sh
```

If the script exits without error, the module passes basic Terraform validation.
