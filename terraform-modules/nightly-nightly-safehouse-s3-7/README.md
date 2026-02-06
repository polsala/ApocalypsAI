# Nightly Safehouse S3 Terraform Module

A whimsical yet practical Terraform module that creates an S3 bucket configured for versioning, server‑side encryption, and a lifecycle rule that expires objects after 365 days. It also generates a random password stored in AWS Secrets Manager for post‑apocalyptic data access.

## Usage

```hcl
module "safehouse_s3" {
  source = "github.com/yourorg/ApocalypsAI//terraform-modules/nightly-safehouse-s3"

  bucket_name = "my-safehouse-bucket"
  region      = "us-east-1"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `region` (string, default `"us-east-1"`): AWS region.
- `expiration_days` (number, default `365`): Days after which objects are deleted.

## Outputs

- `bucket_arn`: ARN of the created bucket.
- `password_secret_arn`: ARN of the Secrets Manager secret containing the random password.

## Testing

Run the test script:

```sh
cd tests && ./validate.sh
```
